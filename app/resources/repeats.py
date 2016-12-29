"""Repeat resource"""

from flask import request

from flask_restplus import Resource

from .. import api
from ..models import Repeat, User
from ..schemas import RepeatSchema
from ..util import helpers, auth
from .. import limiter


class RepeatList(Resource):
    """
    Lists all the repeats. Has to be defined separately because of how
    Flask-RESTPlus works.
    """

    @limiter.limit("1000/day;90/hour;20/minute")
    @auth.scopes_required({"repeat:details", "repeat:list"})
    @helpers.check_limit
    @helpers.lower_kwargs("token")
    def get(self, path_data, **kwargs):
        data = {**path_data, **kwargs}
        attributes, errors, code = helpers.multi_response(
            "repeat", Repeat, **data)

        response = {}

        if errors != []:
            response["errors"] = errors
        else:
            response["data"] = attributes

        return response, code


class RepeatResource(Resource):

    @limiter.limit("1000/day;90/hour;20/minute")
    @auth.scopes_required({"repeat:details"})
    @helpers.lower_kwargs("token", "repeatName")
    def get(self, path_data, **kwargs):
        attributes, errors, code = helpers.single_response(
            "repeat", Repeat, **path_data)

        response = {}

        if errors == {}:
            response["data"] = attributes
        else:
            response["errors"] = errors

        return response, code

    @limiter.limit("1000/day;90/hour;20/minute")
    @auth.scopes_required({"repeat:details", "repeat:create",
                           "repeat:manage"})
    @helpers.lower_kwargs("token", "repeatName")
    def patch(self, path_data, **kwargs):
        data = helpers.get_mixed_args()

        if data is None:
            return {"errors": ["Bro...no data"]}, 400

        data = {**data,
                **path_data,
                "repeatId": helpers.next_numeric_id(
                    "repeat",
                    id_field="repeatId",
                    **path_data
                )}

        # TODO: Refactor this
        command_name = data.get("commandName")
        if command_name is None:
            return {"errors": ["Missing required key 'commandName'"]}, 400

        cmd = helpers.get_one("command",
                              token=data["token"],
                              name=command_name
                              )

        # The command to be aliased doesn't actually exist
        if cmd == {}:
            return {"errors": ["Command to be repeated does not exist!"]}, 400

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
