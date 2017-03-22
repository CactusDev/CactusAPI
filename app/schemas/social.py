from marshmallow import Schema, fields
from datetime import datetime


class SocialSchema(Schema):
    id = fields.String()
    token = fields.String(required=True)
    service = fields.String(required=True)
    url = fields.String(required=True)
    createdAt = fields.DateTime(
        "%c", default=datetime.utcnow().strftime("%c"), dump_only=True)
