"""Command alias resource"""

from flask import request

from flask_restplus import Resource, marshal

from .. import api
from ..models import Alias, User
from ..schemas import CmdAliasSchema
from ..util import helpers


class AliasResource(Resource):

    @helpers.lower_kwargs("token", "aliasName")
    def get(self, path_data, **kwargs):
        attributes, errors, code = helpers.single_response(
            "aliases", Alias, **path_data)

        response = {}

        if errors == {}:
            response["data"] = attributes
        else:
            response["errors"] = errors

        if attributes != {} and isinstance(attributes, dict):
            # Take attributes, convert "command" to obj
            cmd_id = attributes["attributes"]["command"]
            attributes["attributes"]["command"] = helpers.get_one("command",
                                                                  uid=cmd_id)

        return response, code

    @helpers.lower_kwargs("token", "aliasName")
    def patch(self, path_data, **kwargs):
        data = helpers.get_mixed_args()

        if data is None:
            return {"errors": ["Bro...no data"]}, 400

        data = {**data, **path_data}

        command_name = data.get("command")
        if command_name is None:
            return {"errors": ["Missing required key 'command'"]}

        cmd = helpers.get_one("command",
                              token=data["token"],
                              name=command_name
                              )

        # The command to be aliased doesn't actually exist
        if cmd == {}:
            return {"errors": ["Command to be aliased does not exist!"]}, 404

        # TODO: Make secondary PATCH requests change command to Rethink UUID
        attributes, errors, code = helpers.create_or_update(
            "aliases", Alias, data, "token", "aliasName"
        )

        response = {}

        if errors == {}:
            # Convert "command" to obj
            attributes["attributes"]["command"] = cmd
            response["data"] = attributes
        else:
            response["errors"] = errors

        if code == 201:
            response["meta"] = {"created": True}
        elif code == 200:
            response["meta"] = {"edited": True}

        return response, code

    @helpers.lower_kwargs("token", "aliasName")
    def delete(self, path_data, **kwargs):
        deleted = helpers.delete_record("aliases", **path_data)

        if deleted is not None:
            return {"meta": {"deleted": deleted}}, 200
        else:
            return None, 404
