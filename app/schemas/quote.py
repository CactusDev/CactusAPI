from datetime import datetime
from marshmallow import Schema, fields

from ..util import helpers


class QuoteSchema(Schema):
    id = fields.String()
    quote = fields.String(required=True)
    quoteId = fields.Integer(required=True)
    token = fields.String(required=True)
    enabled = fields.Boolean()
    createdAt = fields.DateTime(
        "%c", default=datetime.utcnow().strftime("%c"), dump_only=True)
    deletedAt = fields.Float(default=None, allow_none=True)
