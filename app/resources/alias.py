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
        # TODO: Fix the table generation so it doesn't require second 's'
        attributes, errors, code = helpers.single_response(
            "aliass", Alias, **path_data)

        # Take attributes, convert "command" to obj
        cmd_id = attributes["attributes"]["command"]
        attributes["attributes"]["command"] = helpers.get_one("command",
                                                              uid=cmd_id)
        response = {}

        if errors == {}:
            response["data"] = attributes
        else:
            response["errors"] = errors

        return response, code

    @helpers.lower_kwargs("token", "aliasName")
    def patch(self, path_data, **kwargs):
        json_data = request.get_json()

        if json_data is None:
            return {"errors": ["Bro...no data"]}, 400

        data = {**json_data, **path_data}

        # TODO: Fix the table generation so it doesn't require second 's'
        attributes, errors, code = helpers.create_or_update(
            "aliass", Alias, data, ["token", "aliasName"]
        )

        # Take attributes, convert "command" to obj
        cmd_id = attributes["attributes"]["command"]
        attributes["attributes"]["command"] = helpers.get_one("command",
                                                              uid=cmd_id)

        response = {}

        if code == 201:
            response["meta"] = {"created": True}
        elif code == 200:
            response["meta"] = {"edited": True}

        if errors == {}:
            response["data"] = attributes
        else:
            response["errors"] = errors

        return response, code

    @helpers.lower_kwargs("token", "aliasName")
    def delete(self, path_data, **kwargs):
        deleted = helpers.delete_record("aliass", **path_data)

        if deleted is not None:
            return {"meta": {"deleted": deleted}}, 200
        else:
            return None, 404
