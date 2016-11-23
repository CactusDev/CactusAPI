from marshmallow import Schema, fields


class QuoteSchema(Schema):
    # TODO:150 Figure out how to use underscore_case for fields
    # dump_to="newName" works, but it's got all sorts of issues
    id = fields.String()
    quote = fields.String(required=True)
    quoteId = fields.Integer(required=True)
    token = fields.String(required=True)
    enabled = fields.Boolean()
    createdAt = fields.DateTime()
