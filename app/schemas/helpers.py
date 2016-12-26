from marshmallow import fields, ValidationError, Schema
import re

from ..util import helpers


class MessagePacketSchema(Schema):
    type = fields.String(required=True)
    data = fields.String(required=True)
    text = fields.String(required=True)


class CommandUUID(fields.Field):

    def _deserialize(self, value, attr, obj):
        if not helpers.validate_uuid4(value):
            # Get the command UUID for the alias's command
            value = helpers.get_one(
                "command",
                token=obj["token"],
                name=obj["command"]
            )["id"]

            obj["command"] = value

        return value


class ValidateToken(fields.Field):

    def _serialize(self, value, attr, obj):
        valid_token = re.fullmatch(r"\w{1,32}", value)

        if valid_token is None:
            raise ValidationError("token is not valid")

        return value
