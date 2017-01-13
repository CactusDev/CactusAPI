"""Repeat resource"""

from flask import request

from flask_restplus import Resource

from .. import api
from ..models import Repeat, User
from ..schemas import RepeatSchema
from ..util import helpers, auth
from ..util.helpers import APIError
from .. import limiter


class RepeatList(Resource):
    """
    Lists all the repeats. Has to be defined separately because of how
    Flask-RESTPlus works.
    """

    @limiter.limit("1000/day;90/hour;20/minute")
    @helpers.check_limit
    @helpers.lower_kwargs("token")
    def get(self, path_data, **kwargs):
        data = {**path_data, **kwargs}
        attributes, errors, code = helpers.multi_response(
            "repeats", Repeat, **data)

        for repeat in attributes:
            cmd = helpers.get_one("command",
                                  name=repeat["attributes"]["commandName"],
                                  token=path_data["token"]
                                  )

            # No custom command matches that
            if cmd == {}:
                cmd, errors, code = helpers.alias_then_builtins(
                    name=repeat["attributes"]["commandName"],
                    token=path_data["token"]
                )

            repeat["attributes"]["command"] = cmd

        response = {}

        if errors != [] and errors != {}:
            response["errors"] = errors
        else:
            response["data"] = attributes

        return response, code


class RepeatResource(Resource):

    @limiter.limit("1000/day;90/hour;20/minute")
    @helpers.lower_kwargs("token", "repeatName")
    def get(self, path_data, **kwargs):
        attributes, errors, code = helpers.single_response(
            "repeats", Repeat, **path_data)

        if code != 404:
            cmd = helpers.get_one("command",
                                  name=attributes["attributes"]["commandName"],
                                  token=path_data["token"]
                                  )

            # No custom command matches that
            if cmd == {}:
                cmd, errors, _ = helpers.alias_then_builtins(
                    name=attributes["attributes"]["commandName"],
                    token=path_data["token"]
                )
        else:
            cmd = attributes

        response = {}

        # TODO: Can this be cleaned up? Probably.
        if errors == {}:
            if code == 404:
                response["data"] = {}
            else:
                # Convert "command" to obj
                attributes["attributes"]["command"] = cmd
                response["data"] = attributes
        else:
            response["errors"] = errors

        return response, code

    @limiter.limit("1000/day;90/hour;20/minute")
    @auth.scopes_required({"repeat:create", "repeat:manage"})
    @helpers.lower_kwargs("token", "repeatName")
    @helpers.catch_api_error
    def patch(self, path_data, **kwargs):
        data = {**helpers.get_mixed_args(),
                **path_data,
                "repeatId": helpers.next_numeric_id(
                    "repeat",
                    id_field="repeatId",
                    **path_data
        )}

        # TODO: Refactor this
        command_name = data.get("commandName")
        if command_name is None:
            raise APIError("Missing required key 'commandName'", code=400)

        cmd = helpers.get_one("command",
                              token=data["token"],
                              name=command_name
                              )
        # No custom command matches that
        if cmd == {}:
            cmd, errors, code = helpers.alias_then_builtins(
                name=command_name
            )

            if code == 404:
                raise APIError("Command to be repeated does not exist!",
                               code=400)

        attributes, errors, code = helpers.create_or_update(
            "repeat", Repeat, data, "token", "commandName", post=True)

        response = {}

        if errors == {}:
            # Convert "command" to obj
            attributes["attributes"]["command"] = cmd
            response["data"] = attributes
        else:
            response["errors"] = errors

        return response, code

    @limiter.limit("1000/day;90/hour;20/minute")
    @auth.scopes_required({"repeat:manage"})
    @helpers.lower_kwargs("token", "repeatName")
    def delete(self, path_data, **kwargs):
        deleted = helpers.delete_record("repeat", **path_data)

        if deleted is not None:
            return {"meta": {"deleted": deleted}}, 200
        else:
            return None, 404
