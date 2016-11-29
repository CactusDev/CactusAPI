from marshmallow import Schema, fields, pre_load, pre_dump, post_dump, post_load

from . import CommandSchema

from ..util import helpers


class CommandUUID(fields.Field):

    def _deserialize(self, value, attr, obj):
        if not helpers.validate_uuid4(value):
            # Get the command UUID for the alias's command
            value = helpers.get_one(
                "command",
                **{
                    "token": obj["token"],
                    "name": obj["command"]
                }
            )["id"]

            obj["command"] = value

        return value


class CmdAliasSchema(Schema):
    id = fields.String()
    aliasName = fields.String(required=True)
    createdAt = fields.DateTime()
    token = fields.String(required=True)
    command = CommandUUID()
