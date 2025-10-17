from marshmallow import fields, Schema

class DocsPostSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str()
    content = fields.Str()