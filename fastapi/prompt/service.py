from main import app

from outlines import from_openai
from pydantic import BaseModel

from ir.schema import IR

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
        for api in ir['apis']:
            print(api.get('method'), api.get('path'))
            print(api.get('operation'), api.get('entity'))
            print('Request Fields:', api.get('request_fields'))
            print('Response Fields:', api.get('response_fields'))
            print('-------')

        for entity in ir['entities']:
            print(entity.get('name'))
            for field in entity.get('fields'):
                print(field)
            print('-------')

        return {"message": f"Prompt '{prompt}' created successfully."}