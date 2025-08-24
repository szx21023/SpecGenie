from marshmallow import fields, Schema

class PromptSchema(Schema):
    id = fields.Int(dump_only=True)
    prompt = fields.Str(required=True)

# fastapi/planner/schema.py
from typing import List, Literal, Optional, Union, Annotated
from pydantic import BaseModel, Field

class ColumnDef(BaseModel):
    name: str
    type: str
    nullable: bool

class TableSelector(BaseModel):
    by: Literal["id","name"]
    value: str

class ApiSelector(BaseModel):
    by: Literal["id","path"]
    value: str

class AddTable(BaseModel):
    kind: Literal["add_table"]
    name: str
    columns: List[ColumnDef]

class UpdateTable(BaseModel):
    kind: Literal["update_table"]
    target: TableSelector
    final_columns: List[ColumnDef]
    # add_columns: List[ColumnDef]
    # update_columns: List[ColumnDef]
    # drop_columns: List[str]

class DropTable(BaseModel):
    kind: Literal["drop_table"]
    target: TableSelector
    if_exists: bool

class AddApi(BaseModel):
    kind: Literal["add_api"]
    method: str
    path: str
    request_fields: List[str]
    response_fields: List[str]

class UpdateApi(BaseModel):
    kind: Literal["update_api"]
    target: ApiSelector
    final_request_fields: List[str]
    final_response_fields: List[str]
    # add_request_fields: List[str]
    # drop_request_fields: List[str]
    # add_response_fields: List[str]
    # drop_response_fields: List[str]

class DropApi(BaseModel):
    kind: Literal["drop_api"]
    target: ApiSelector
    if_exists: bool

class Plan(BaseModel):
    operations: List[UpdateTable | AddTable | DropTable | AddApi | UpdateApi | DropApi]