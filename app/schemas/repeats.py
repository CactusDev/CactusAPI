from marshmallow import Schema, fields, pre_load, pre_dump, post_load
from . import CommandSchema
from ..util import helpers


class RepeatSchema(Schema):
    # TODO:150 Figure out how to use underscore_case for fields
    # dump_to="newName" works, but it's got all sorts of issues
    id = fields.String()
    period = fields.Integer(required=True, default=900)
    token = fields.String(required=True)
    repeatId = fields.Integer(required=True)
    commandName = fields.String(required=True)
    command = fields.Nested(CommandSchema, dump_only=True, required=True)

    @pre_load
    def get_command_id(self, data):
        """Gets the command UUID for the repeat's command"""
        data["command"] = helpers.get_one(
            "command",
            **{
                "token": data["token"],
                "name": data["commandName"]
            }
        )["id"]

        return data

    @pre_dump
    def id_to_obj(self, obj):
        """Gets the command object associated with the stored command ID"""
        cmd = helpers.get_one("command", uid=obj.command)
        # Remove createdAt and id keys from command because they're not needed
        del cmd["createdAt"], cmd["id"]

        obj.command = cmd

        return obj
