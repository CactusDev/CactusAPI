from marshmallow import Schema, fields
from datetime import datetime

from ..util import helpers


class TrustSchema(Schema):
    id = fields.String()
    userName = fields.String(required=True)
    userId = fields.String(required=True)
    active = fields.Boolean()
    token = fields.String(required=True)
    createdAt = fields.DateTime(
        "%c", default=datetime.utcnow().strftime("%c"), dump_only=True)
