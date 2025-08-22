from main import app
from sqlalchemy import select

from outlines import from_openai
from pydantic import BaseModel

from ir.schema import IR
from ir.service import IRService
from apis.service import ApisService
from tables.service import TablesService

from .model import Prompts
from .schema import PromptSchema

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

        ir = await PromptService.prompt(db, prompt, IR)
        result = await IRService.create_ir(db, ir)

        for api in result['apis']:
            await ApisService.create_api(db, api)

        for entity in result['entities']:
            await TablesService.create_table(db, entity)

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

        return result

    @staticmethod
    async def get_prompts(db):
        sql = select(Prompts)
        result = await db.execute(sql)
        prompts = result.scalars().all()

        schema = PromptSchema(many=True)
        prompts = schema.dump(prompts)
        return prompts