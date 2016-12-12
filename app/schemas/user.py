from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.String()
    token = fields.String(required=True)
    userName = fields.String(required=True)
    userId = fields.Integer(required=True)
    service = fields.String(required=True, default="beam")
