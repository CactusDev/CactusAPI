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
    @helpers.catch_api_error
    def get(self, **kwargs):
        attributes, errors, code = helpers.single_response(
            "aliases", Alias, cased="name",
            **{"name": kwargs["name"], "token": kwargs["token"].lower()})

        response = {}

        if errors == {}:
            response["data"] = attributes
        else:
            response["errors"] = errors

        if attributes != {} and isinstance(attributes, dict):
            # Take attributes, convert "command" to obj
            cmd_id = attributes["attributes"]["command"]
            cmd = helpers.get_one("command", uid=cmd_id)
            if cmd == {}:
                cmd = helpers.get_one("builtins", uid=cmd_id)
            if cmd == {}:
                # There was no builtin or custom command that matched
                raise APIError("Alias exists but aliased command does not")
            attributes["attributes"]["command"] = cmd

        return response, code

    @limiter.limit("1000/day;90/hour;20/minute")
    @auth.scopes_required({"alias:create", "alias:manage"})
    @helpers.catch_api_error
    def patch(self, **kwargs):
        lookup_data = {"token": kwargs["token"].lower(),
                       "name": kwargs["name"]}
        data = {**helpers.get_mixed_args(), **lookup_data}

        command_name = data.get("commandName")
        if command_name is None:
            raise APIError("Missing required key 'commandName'", code=400)

        if data.get("id") is not None:
            del data["id"]

        cmd_exists = helpers.get_one("command", **lookup_data)

        if cmd_exists != {}:
            raise APIError(
                "Command already exists with the requested alias name",
                code=400)

        cmd = helpers.get_one("command",
                              token=data["token"], name=command_name)

        # The command to be aliased doesn't actually exist
        # caused by _deserialize method in schema
        if cmd == {}:
            # Check if a builtin exists for it
            cmd = helpers.get_one("builtins", name=command_name)

            if cmd == {}:
                raise APIError("Command to be aliased does not exist!",
                               code=404)

        data["command"] = cmd["id"]

        # TODO: Make secondary PATCH requests change command to Rethink UUID
        attributes, errors, code = helpers.create_or_update(
            "aliases", Alias, data,
            token=kwargs["token"].lower(), name=kwargs["name"],
            cased={"key": "name", "value": kwargs["name"]}
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

    @limiter.limit("1000/day;90/hour;20/minute")
    @auth.scopes_required({"alias:manage"})
    def delete(self, **kwargs):
        deleted = helpers.delete_record("aliases", name=kwargs["name"])

        if deleted is not None and deleted != []:
            return {"meta": {"deleted": deleted}}, 200
        else:
            return None, 404
