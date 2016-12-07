from marshmallow import fields

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
