from marshmallow import Schema, fields


class SocialSchema(Schema):
    id = fields.String()
    token = fields.String(required=True)
    service = fields.String(required=True)
    url = fields.Url(required=True)
