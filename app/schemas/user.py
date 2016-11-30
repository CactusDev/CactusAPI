from marshmallow import Schema, fields, post_load


class UserSchema(Schema):
    id = fields.String()
    token = fields.String(required=True)
    newCommandId = fields.Integer()
