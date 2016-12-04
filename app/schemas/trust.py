from marshmallow import Schema, fields, pre_dump, post_dump
from dateutil import parser

from ..util import helpers


class TrustSchema(Schema):
    id = fields.String()
    userName = fields.String(required=True)
    userId = fields.String(required=True)
    active = fields.Boolean()
    token = fields.String(required=True)
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
