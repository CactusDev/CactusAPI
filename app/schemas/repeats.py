from marshmallow import Schema, fields, pre_dump, post_dump
from . import CommandSchema
from .helpers import CommandUUID
from dateutil import parser

from ..util import helpers


class RepeatSchema(Schema):
    id = fields.String()
    period = fields.Integer(required=True, default=900)
    token = fields.String(required=True)
    repeatId = fields.Integer(required=True)
    command = CommandUUID()

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
