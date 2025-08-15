from marshmallow import fields, Schema

class TableColumnSchema(Schema):
    name = fields.Str(required=True)
    type = fields.Str(required=True)
    nullable = fields.Bool(required=True)

class TablesSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    columns = fields.List(fields.Nested(TableColumnSchema), required=True)