from main import app

from outlines import from_openai
from openai import OpenAI
from pydantic import BaseModel
from typing import List

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

        class Field(BaseModel):
            name: str
            type: str
            primary: bool
            foreign_key: str  # 如果不能為空，這樣寫；若允許 null 要加特別處理

        class Entity(BaseModel):
            name: str
            fields: List[Field]

        class API(BaseModel):
            method: str
            path: str
            operation: str
            entity: str
            request_fields: List[str]
            response_fields: List[str]

        class IR(BaseModel):
            entities: List[Entity]
            apis: List[API]

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