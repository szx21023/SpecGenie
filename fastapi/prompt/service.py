from main import app

from outlines import from_openai
from openai import OpenAI
from pydantic import BaseModel
from typing import List

class PromptService:
    @staticmethod
    async def create_prompt(db, prompt: str):
        """
        Create a new prompt with the given title.
        """
        # Create the model
        model = from_openai(
            OpenAI(api_key=app.state.config.get("OPENAI_API_KEY")),
            "gpt-4o"
        )

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

        ir_result = model(
            "我要建立一個系統來管理使用者與書籍，並記錄誰借了哪些書。",
            IR
        )

        ir = IR.model_validate_json(ir_result)
        for entity in ir.model_dump()['entities']:
            print(entity.get('name'))
            for field in entity.get('fields'):
                print(field)
            print('-------')

        return {"message": f"Prompt '{prompt}' created successfully."}