from marshmallow import Schema, fields, pre_load, pre_dump, post_dump, post_load
from dateutil import parser

from . import CommandSchema
from .helpers import CommandUUID
from ..util import helpers


class CmdAliasSchema(Schema):
    id = fields.String()
    aliasName = fields.String(required=True)
    createdAt = fields.DateTime()
    token = fields.String(required=True)
    command = CommandUUID()
    arguments = fields.List(fields.String())

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
