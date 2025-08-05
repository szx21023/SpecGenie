from pydantic import BaseModel
from typing import List

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