from marshmallow import Schema, fields, pre_dump, post_dump
from . import CommandSchema
from .helpers import CommandUUID
from datetime import datetime

from ..util import helpers


class RepeatSchema(Schema):
    id = fields.String()
    period = fields.Integer(required=True, default=900)
    token = fields.String(required=True)
    repeatName = fields.String(required=True)
    command = CommandUUID()
    commandName = fields.String(required=True)
    createdAt = fields.DateTime(
        "%c", default=datetime.utcnow().strftime("%c"), dump_only=True)
