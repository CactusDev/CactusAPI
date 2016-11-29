from marshmallow import Schema, fields, pre_dump

from . import CommandSchema
from .helpers import CommandUUID

from ..util import helpers


class CmdAliasSchema(Schema):
    id = fields.String()
    aliasName = fields.String(required=True)
    # TODO: Post feature-freeze, figure out how to implement properly w/
    # fields.DateTime
    createdAt = fields.String()
    token = fields.String(required=True)
    command = CommandUUID()

    @pre_dump
    def convert_datetime(self, data):
        if hasattr(data, "createdAt"):
            data.createdAt = helpers.humanize_datetime_single(data.createdAt)

        return data
