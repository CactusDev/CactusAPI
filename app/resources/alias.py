"""Command alias resource"""

from flask import request

from flask_restplus import Resource, marshal

from .. import api
from ..models import Alias, User
from ..schemas import CmdAliasSchema
from ..util import helpers, auth
from ..util.helpers import APIError
from .. import limiter


class AliasResource(Resource):

    @limiter.limit("1000/day;90/hour;20/minute")
    @helpers.check_limit
    @helpers.lower_kwargs("token", "name")
    def get(self, path_data, **kwargs):
        attributes, errors, code = helpers.single_response(
            "aliases", Alias, **{**kwargs, **path_data})

        if code != 404:
            command = helpers.uid_to_object(
                "commands",
                attributes["attributes"]["command"],
                "name"
            )

            # It's not a custom command, must be a builtin
            if command == {}:
                command = helpers.uid_to_object(
                    "builtins",
                    attributes["attributes"]["command"],
                    "name"
                )

            attributes["attributes"].update(command)

            del attributes["attributes"]["command"]

        response = {}

        if errors == {}:
            if code != 404:
                attributes["type"] = "alias"
            response["data"] = attributes
        else:
            response["errors"] = errors

        return response, code

    @limiter.limit("1000/day;90/hour;20/minute")
    @auth.scopes_required({"alias:create", "alias:manage"})
    @helpers.lower_kwargs("token", "name")
    @helpers.catch_api_error
    def patch(self, path_data, **kwargs):
        data = {**helpers.get_mixed_args(), **path_data}

        command_name = data.get("commandName")

        if command_name is None:
            raise APIError("Missing required key 'commandName'", code=400)

        cmd_exists = helpers.get_one("commands", **path_data)

        if cmd_exists != {}:
            raise APIError(
                "Command already exists with the requested alias name",
                code=400)

        cmd = helpers.get_one("commands",
                              token=data["token"],
                              name=command_name
                              )

        # Now we're getting the command that the alias is aliasing
        # The command to be aliased doesn't actually exist
        if cmd == {}:
            cmd = helpers.get_one("builtins", name=command_name)
            if cmd == {}:
                raise APIError(
                    "Command to be aliased does not exist!", code=404)

        data["command"] = cmd["id"]

        # TODO: Make secondary PATCH requests change command to Rethink UUID
        attributes, errors, code = helpers.create_or_update(
            "aliases", Alias, data, "token", "name"
        )

        response = {}

        if errors == {}:
            if code != 404:
                attributes["type"] = "alias"
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

    @limiter.limit("1000/day;90/hour;20/minute")
    @auth.scopes_required({"alias:manage"})
    @helpers.lower_kwargs("token", "name")
    def delete(self, path_data, **kwargs):
        deleted = helpers.delete_record("aliases", **path_data)

        if deleted is not None:
            return {"meta": {"deleted": deleted}}, 200
        else:
            return None, 404
