from marshmallow import fields, Schema

class PromptSchema(Schema):
    id = fields.Int(dump_only=True)
    prompt = fields.Str(required=True)