from marshmallow import fields, Schema

class RagVectorSchema(Schema):
    id = fields.Str()
    source_type = fields.Str()
    source_id = fields.Str()
    mode = fields.Str()
    role = fields.Str()
    text = fields.Str()
    embedding = fields.List(fields.Float())