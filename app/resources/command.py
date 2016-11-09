from flask import request, make_response, g

from flask_restplus import Resource, marshal

from datetime import datetime

from .. import api
from ..models import Command, User
from ..schemas import CommandSchema
from ..util import helpers


class CommandList(Resource):
    """
    Lists all the commands. Has to be defined separately because of how
    Flask-RESTPlus works.
    """

    def get(self, **kwargs):
        response, errors, code = helpers.multi_response(
            "command", Command, {"token": kwargs["token"].lower()})

        return {"data": response, "errors": errors}, code


class CommandResource(Resource):
    # TODO: Move repetitive kwargs parsing into function/decorator

    def get(self, **kwargs):
        """/api/v1/:token/command/:command -> [int ID | str Name]"""

        token = kwargs["token"].lower()

        # TODO:210 Implement cross-platform regex for checking valid tokens.
        # Currently just looking to see if anything exists with that token
        # if not helpers.is_valid_token(token):
        # return {"errors": "doom and stuff. Probably some death too."}, 400

        path_data = {"token": token}

        if kwargs["command"].isdigit():
            path_data["commandId"] = int(kwargs["command"])

            # If a command for this user (via token) matches the numeric ID
            # given, then retrieve the name of that command
            if helpers.exists("command", **path_data):
                path_data["name"] = helpers.get_one(
                    "command", **path_data)["name"]
        else:
            path_data["name"] = kwargs["command"].lower()

            # If a command exists for this user (via token) that matches
            # the name given, retrieve the numeric ID for it
            if helpers.exists("command", **path_data):
                path_data["commandId"] = helpers.get_one(
                    "command", **path_data)["commandId"]

        response, errors, code = helpers.single_response(
            "command", Command, path_data)

        return {"data": response, "errors": errors}, code

    def patch(self, **kwargs):
        token = kwargs["token"].lower()

        # if not helpers.exists("commands", token=token):
        # return {"errors": ["doom and stuff. Probably some death too"]}, 400

        # TODO:220 Implement cross-platform regex for checking valid tokens.
        # Currently just looking to see if anything exists with that token
        # if not helpers.is_valid_token(token):
        # return {"errors": "doom and stuff. Probably some death too."}, 400

        path_data = {"token": token}

        if kwargs["command"].isdigit():
            path_data["commandId"] = int(kwargs["command"])

            # If a command for this user (via token) matches the numeric ID
            # given, then retrieve the name of that command
            if helpers.exists("command", **path_data):
                path_data["name"] = helpers.get_one(
                    "command", **path_data)["name"]
        else:
            path_data["name"] = kwargs["command"].lower()

            # If a command exists for this user (via token) that matches
            # the name given, retrieve the numeric ID for it
            if helpers.exists("command", **path_data):
                path_data["commandId"] = helpers.get_one(
                    "command", **path_data)["commandId"]
            else:
                # OR, since the command doesn't exist yet, retrieve the next
                # numeric ID for that user
                path_data["commandId"] = helpers.get_one(
                    "user", token=token.lower())["newCommandId"]

        json_data = request.get_json()

        if json_data is None:
            return {"errors": ["Bro...no data"]}, 400

        data = {**json_data, **path_data}

        response, errors, code = helpers.create_or_update(
            "command", Command, data, ["commandId", "token"]
        )

        if code == 201:
            # Increase the newCommandId for this user since a commmand was
            # succesfully completed
            helpers.increment_counter("user", {"token": token}, "newCommandId")

        return {"data": response, "errors": errors}, code

    def delete(self, **kwargs):
        token = kwargs["token"].lower()

        data = {"token": token}
        if kwargs["command"].isdigit():
            data["commandId"] = int(kwargs["command"])

            # If a command for this user (via token) matches the numeric ID
            # given, then retrieve the name of that command
            if helpers.exists("command", **data):
                data["name"] = helpers.get_one(
                    "command", **data)["name"]
        else:
            data["name"] = kwargs["command"].lower()

            # If a command exists for this user (via token) that matches
            # the name given, retrieve the numeric ID for it
            if helpers.exists("command", **data):
                data["commandId"] = helpers.get_one(
                    "command", **data)["commandId"]

        deleted = helpers.delete_record("command", **data)

        if deleted is not None:
            return {"meta": {"deleted": deleted}}, 200
        else:
            return None, 404
