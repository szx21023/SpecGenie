from marshmallow import fields, Schema

class ApisSchema(Schema):
    id = fields.Int(dump_only=True)
    method = fields.Str(required=True)
    path = fields.Str(required=True)
    request_fields = fields.List(fields.Str(), required=True)
    response_fields = fields.List(fields.Str(), required=True)
