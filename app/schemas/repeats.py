from marshmallow import (Schema, fields, pre_dump, validates,
                         post_dump, ValidationError)
from . import CommandSchema
from .helpers import CommandUUID
from datetime import datetime

from ..util import helpers


class RepeatSchema(Schema):
    id = fields.String()
    period = fields.Integer(required=True, default=60000)
    token = fields.String(required=True)
    repeatName = fields.String(required=True)
    command = CommandUUID()
    commandName = fields.String(required=True)
    createdAt = fields.DateTime(
        "%c", default=datetime.utcnow().strftime("%c"), dump_only=True)

    @validates("period")
    def foo(self, data):
        if data < 60000:
            raise ValidationError("Minimum time for a repeat is 1 minute "
                                  "(60000 milliseconds)")
