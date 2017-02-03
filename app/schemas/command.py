from marshmallow import (Schema, fields, post_dump,
                         pre_dump, validates, ValidationError)
from datetime import datetime

from ..util import helpers
from .helpers import MessagePacketSchema


class ResponseSchema(Schema):
    message = fields.Nested(MessagePacketSchema, many=True)
    user = fields.String()
    action = fields.Boolean()
    target = fields.String(allow_none=True)
    role = fields.Integer(default=0)

    @validates('message')
    def validate_message(self, value):
        if value == []:
            raise ValidationError("Response's message must have at least one "
                                  "valid message packet")


class CommandSchema(Schema):
    id = fields.String()
    name = fields.String(required=True)
    response = fields.Nested(ResponseSchema, required=True)
    createdAt = fields.DateTime(
        "%c", default=datetime.utcnow().strftime("%c"), dump_only=True)
    token = fields.String(required=True)
    enabled = fields.Boolean(default=True)
    arguments = fields.Nested(MessagePacketSchema, many=True)
    count = fields.Integer(default=0)

    # @pre_dump
    # def rethink_to_dt_obj(self, obj):
    #     if hasattr(obj, "createdAt"):
    #         obj.createdAt = parser.parse(obj.createdAt)
    #
    #     return obj
    #
    # @post_dump
    # def humanize_datetime(self, data):
    #     if "createdAt" in data:
    #         data["createdAt"] = helpers.humanize_datetime(data["createdAt"])
    #
    #     return data
