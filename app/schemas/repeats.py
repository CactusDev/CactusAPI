from marshmallow import Schema, fields
from . import CommandSchema
from ..util import helpers

from .helpers import CommandUUID


class RepeatSchema(Schema):
    # TODO:150 Figure out how to use underscore_case for fields
    # dump_to="newName" works, but it's got all sorts of issues
    id = fields.String()
    period = fields.Integer(required=True, default=900)
    token = fields.String(required=True)
    repeatId = fields.Integer(required=True)
    command = CommandUUID()
