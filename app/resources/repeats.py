"""Repeat resource"""

from flask import request

from flask_restplus import Resource

from .. import api
from ..models import Repeat, User
from ..schemas import RepeatSchema
from ..util import helpers


class RepeatList(Resource):
    """
    Lists all the repeats. Has to be defined separately because of how
    Flask-RESTPlus works.
    """

    @helpers.lower_kwargs("token")
    def get(self, path_data, **kwargs):
        attributes, errors, code = helpers.multi_response(
            "repeat", Repeat, **path_data)

        # TODO: Make this nice. Because this is positively repulsive
        if code == 200:
            for result in attributes:
                # Take attributes, convert "command" to obj
                cmd_id = result["attributes"]["command"]
                cmd = helpers.get_one("command", uid=cmd_id)
                del cmd["createdAt"], cmd["id"]
                result["attributes"]["command"] = cmd

        response = {}

        if errors != []:
            response["errors"] = errors
        else:
            response["data"] = attributes

        return response, code

    @helpers.lower_kwargs("token")
    def post(self, path_data, **kwargs):
        # TODO:220 Implement cross-platform regex for checking valid tokens
        # TODO Make endpoint 400 if the command provided doesn't exist
        json_data = request.get_json()

        if json_data is None:
            return {"errors": ["Bro...no data"]}, 400

        data = {**json_data,
                **path_data,
                "repeatId": helpers.next_numeric_id(
                    "repeat",
                    id_field="repeatId",
                    **path_data
                )}

        attributes, errors, code = helpers.create_or_none(
            "repeat", Repeat, data, ["token"])

        # TODO: Make this nice. Because this is positively repulsive
        if code == 200:
            # Take attributes, convert "command" to obj
            cmd_id = attributes["attributes"]["command"]
            cmd = helpers.get_one("command", uid=cmd_id)
            del cmd["createdAt"], cmd["id"]
            attributes["attributes"]["command"] = cmd

        response = {}

        if errors == {}:
            response["data"] = attributes
        else:
            response["errors"] = errors

        return response, code


class RepeatResource(Resource):

    # TODO: Finish moving all @helpers.lower_kwargs to new version
    @helpers.lower_kwargs("token", "repeatId")
    # TODO: Remove all path_data={} and use just path_data
    def get(self, path_data, **kwargs):
        attributes, errors, code = helpers.single_response(
            "repeat", Repeat, **path_data)

        # TODO: Make this nice. Because this is positively repulsive
        if code == 200:
            # Take attributes, convert "command" to obj
            cmd_id = attributes["attributes"]["command"]
            cmd = helpers.get_one("command", uid=cmd_id)
            del cmd["createdAt"], cmd["id"]
            attributes["attributes"]["command"] = cmd

        response = {}

        if errors == {}:
            response["data"] = attributes
        else:
            response["errors"] = errors

        return response, code

    @helpers.lower_kwargs("token", "repeatId")
    def delete(self, path_data, **kwargs):
        deleted = helpers.delete_record("repeat", **path_data)

        if deleted is not None:
            return {"meta": {"deleted": deleted}}, 200
        else:
            return None, 404
