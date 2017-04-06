from marshmallow import Schema, fields
from datetime import datetime

from ..util import helpers


class PointSchema(Schema):
    id = fields.String()
    username = fields.String(required=True)
    createdAt = fields.DateTime(
        "%c", default=datetime.utcnow().strftime("%c"), dump_only=True)
    token = fields.String(required=True)
    count = fields.Integer(default=0)
