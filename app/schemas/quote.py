from dateutil import parser
from marshmallow import Schema, fields, pre_dump, post_dump

from ..util import helpers


class QuoteSchema(Schema):
    id = fields.String()
    quote = fields.String(required=True)
    quoteId = fields.Integer(required=True)
    token = fields.String(required=True)
    enabled = fields.Boolean()
    createdAt = fields.DateTime()

    @pre_dump
    def rethink_to_dt_obj(self, obj):
        if hasattr(obj, "createdAt"):
            obj.createdAt = parser.parse(obj.createdAt)

        return obj

    @post_dump
    def humanize_datetime(self, data):
        if "createdAt" in data:
            data["createdAt"] = helpers.humanize_datetime(data["createdAt"])

        return data
