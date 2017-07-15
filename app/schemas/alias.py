from marshmallow import Schema, fields, pre_load, pre_dump, post_dump, post_load
from datetime import datetime

from . import CommandSchema
from .helpers import CommandUUID
from ..util import helpers
from .helpers import MessagePacketSchema


class CmdAliasSchema(Schema):
    id = fields.String()
    name = fields.String(required=True)
    createdAt = fields.DateTime(
        "%c", default=datetime.utcnow().strftime("%c"), dump_only=True)
    token = fields.String(required=True)
    command = CommandUUID()
    commandName = fields.String(required=True)
    arguments = fields.Nested(MessagePacketSchema, many=True)
    deletedAt = fields.Float(default=None, allow_none=True)
