"""Repeat resource"""

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
        data = {**kwargs, **path_data}

        attributes, errors, code = helpers.multi_response(
            "repeats", Repeat, **data)

        response = {}

        if errors != []:
            response["errors"] = errors
        else:
            response["data"] = attributes

        return response, code


class RepeatResource(Resource):

    @limiter.limit("1000/day;90/hour;20/minute")
    @helpers.lower_kwargs("token")
    def get(self, path_data, **kwargs):
        data = {**kwargs, **path_data}
        attributes, errors, code = helpers.single_response(
            "repeats", Repeat, **data)

        response = {}

        if attributes != {} and isinstance(attributes, dict):
            # Take attributes, convert "command" to obj
            cmd_id = attributes["attributes"]["command"]
            attributes["attributes"]["command"] = helpers.get_one("command",
                                                                  uid=cmd_id)

        if errors == {}:
            response["data"] = attributes
        else:
            response["errors"] = errors

        return response, code

    @limiter.limit("1000/day;90/hour;20/minute")
    @auth.scopes_required({"repeat:create", "repeat:manage"})
    @helpers.catch_api_error
    def patch(self, **kwargs):
        data = {**helpers.get_mixed_args(),
                "token": kwargs["token"].lower(),
                "repeatId": helpers.next_numeric_id(
                    "repeat",
                    id_field="repeatId",
                    token=kwargs["token"].lower()),
                "repeatName": kwargs["repeatName"]
                }

        if data.get("commandName") is None:
            raise APIError("Missing required key 'commandName'", code=400)
        if data.get("id") is not None:
            del data["id"]

        cmd = helpers.get_one("command",
                              token=data["token"],
                              name=data.get("commandName")
                              )

        # The command to be aliased doesn't actually exist
        if cmd == {}:
            raise APIError("Command to be repeated does not exist!", code=400)

        data["command"] = cmd["id"]

        attributes, errors, code = helpers.create_or_update(
            "repeat", Repeat, data,
            token=kwargs["token"].lower(), repeatName=kwargs["repeatName"]
        )

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
    @helpers.lower_kwargs("token")
    def delete(self, path_data, **kwargs):
        data = {"repeatName": kwargs["repeatName"], **path_data}
        deleted = helpers.delete_record("repeat", **data)

        if deleted is not None:
            return {"meta": {"deleted": deleted}}, 200
        else:
            return None, 404
