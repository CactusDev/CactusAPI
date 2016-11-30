from marshmallow import Schema, fields, post_load


class CommandSchema(Schema):
    id = fields.String()
    title = fields.String(required=True)
    contents = fields.String(required=True)
    flags = fields.Integer(required=True)
    mentions = fields.List(required=True)
    createdAt = fields.DateTime()
