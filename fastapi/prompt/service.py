from main import app
from sqlalchemy import select

from outlines import from_openai
from pydantic import BaseModel

from ir.schema import IR
from ir.service import IRService
from apis.service import ApisService
from tables.service import TablesService

from .model import Prompts
from .schema import PromptSchema, Plan

class PromptService:
    @staticmethod
    async def prompt(db, prompt: str, output_format: BaseModel, model_name: str = "gpt-4o"):
        """
        Create a new prompt with the given prompt.
        """
        # Create the model
        model = from_openai(
            app.state.openai_client,
            model_name
        )

        ir_result = model(
            prompt,
            output_format
        )

        ir = output_format.model_validate_json(ir_result)
        return ir.model_dump()

    @staticmethod
    async def create_prompt(db, prompt: str):
        """
        Test the prompt with the given ID.
        """

        # ir = await PromptService.prompt(db, prompt, IR)
        # result = await IRService.create_ir(db, ir)

        # for api in result['apis']:
        #     await ApisService.create_api(db, api)

        # for entity in result['entities']:
        #     await TablesService.create_table(db, entity)

        schema = PromptSchema()
        data = schema.load({"prompt": prompt})

        prompt = Prompts(**data)
        db.add(prompt)
        try:
            await db.commit()
            await db.refresh(prompt)

        except Exception as e:
            await db.rollback()
            raise e

        return prompt

    @staticmethod
    async def get_prompts(db):
        sql = select(Prompts)
        result = await db.execute(sql)
        prompts = result.scalars().all()

        schema = PromptSchema(many=True)
        prompts = schema.dump(prompts)
        return prompts

    @staticmethod
    async def prompt_to_model(db, prompt: str):
        irs = await IRService.get_ir(db)
        app.logger.info(f'irs: {irs}')
        prompt = prompt + "\n\n" + "目前的規格如下:\n" + str(irs)

        operators = await PromptService.prompt(db, prompt, Plan)
        app.logger.info(operators)
        for operator in operators.get('operations'):
            ops = operator.get('kind')
            by, value = operator.get('target', {}).get('by'), operator.get('target', {}).get('value')
            if ops == 'add_table':
                data = {
                    'name': operator.get('name'),
                    'columns': operator.get('columns', [])
                }
                await TablesService.create_table(db, data)

            elif ops == 'update_table':
                current_table = await PromptService.get_current_spec(irs, 'entity', by, value)
                data = {
                    'columns': operator.get('final_columns', [])
                }
                await TablesService.update_table(db, int(current_table.get('id')), data)

            elif ops == 'drop_table':
                current_table = await PromptService.get_current_spec(irs, 'entity', by, value)
                await TablesService.delete_table(db, int(current_table.get('id')))

            elif ops == 'add_api':
                data = {
                    'method': operator.get('method'),
                    'path': operator.get('path'),
                    'request_fields': operator.get('request_fields', []),
                    'response_fields': operator.get('response_fields', [])
                }
                await ApisService.create_api(db, data)

            elif ops == 'update_api':
                current_api = await PromptService.get_current_spec(irs, 'api', by, value)
                data = {
                    'request_fields': operator.get('final_request_fields', []),
                    'response_fields': operator.get('final_response_fields', [])
                }
                await ApisService.update_api(db, int(current_api.get('id')), data)

            elif ops == 'drop_api':
                current_api = await PromptService.get_current_spec(irs, 'api', by, value)
                await ApisService.delete_api(db, int(current_api.get('id')))

            else:
                pass

        result = PromptService.create_prompt(db, prompt)
        return result

    @staticmethod
    async def get_current_spec(irs, type, by, value):
        if type == 'entity':
            entities = irs.get('entities', [])
            for entity in entities:
                if str(entity.get(by)) != str(value):
                    continue

                return entity

        elif type == 'api':
            apis = irs.get('apis', [])
            for api in apis:
                if str(api.get(by)) != str(value):
                    continue

                return api
