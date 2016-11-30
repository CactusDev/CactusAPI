from marshmallow import Schema, fields


class QuoteSchema(Schema):
    id = fields.String()
    quote = fields.String(required=True)
    quoteId = fields.Integer(required=True)
    token = fields.String(required=True)
    enabled = fields.Boolean()
    createdAt = fields.DateTime()
