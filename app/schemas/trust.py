from marshmallow import Schema, fields


class TrustSchema(Schema):
    id = fields.String()
    userName = fields.String(required=True)
    userId = fields.String(required=True)
    active = fields.Boolean()
    token = fields.String(required=True)
    createdAt = fields.DateTime()
