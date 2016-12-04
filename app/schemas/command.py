from marshmallow import Schema, fields, post_dump, pre_dump
from dateutil import parser

from ..util import helpers


class MessagePacketSchema(Schema):
    type = fields.String(required=True)
    data = fields.String(required=True)
    text = fields.String(required=True)


class ResponseSchema(Schema):
    message = fields.Nested(MessagePacketSchema, many=True, required=True)
    user = fields.String()
    role = fields.Integer()
    action = fields.Boolean()
    target = fields.String(allow_none=True)


class CommandSchema(Schema):
    id = fields.String()
    name = fields.String(required=True)
    response = fields.Nested(ResponseSchema, required=True)
    createdAt = fields.DateTime()
    token = fields.String(required=True)
    userLevel = fields.Integer(required=True)

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
