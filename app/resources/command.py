from flask import request, make_response, g

from flask_restplus import Resource, marshal

from datetime import datetime

from .. import api
from ..models import CommandModel
from ..schemas import CommandSchema
from ..util import helpers

import logging

log = logging.getLogger(__name__)


class CommandList(Resource):
    """
    Lists all the commands. Has to be defined separately because of how
    Flask-RESTPlus works.
    """

    def get(self, **kwargs):
        response, errors, code = helpers.multi_response(
            "commands", CommandModel, {"token": kwargs["token"]})

        return {"data": response, "errors": errors}, code


class CommandResource(Resource):

    def get(self, **kwargs):
        """/api/v1/:token/command/:command -> [int ID | str Name]"""

        token = kwargs["token"]
        command = kwargs["command"]

        if not helpers.exists("commands", token=token):
            return {"errors": ["doom and stuff. Probably some death too"]}, 400

        # TODO: Implement cross-platform regex for checking valid tokens.
        # Currently just looking to see if anything exists with that token
        # if not helpers.is_valid_token(token):
        # return {"errors": "doom and stuff. Probably some death too."}, 400

        path_data = {"token": token}

        if command.isdigit():
            path_data["commandId"] = int(command)
            # TODO: Make this get the associated name from the commands table
            #       If it doesn't exist then there will have to be a name key
            #       in the request JSON
            path_data["name"] = "foo"
        else:
            path_data["name"] = command.lower()
            # TODO: Make this get the associated ID from the commands table
            #       OR make it get the next ID from the user table if
            #       the command with the name provided doesn't exist
            path_data["commandId"] = 1

        response, errors, code = helpers.single_response(
            "command", CommandModel, path_data)

        return {"data": [response], "errors": errors}, code

    def patch(self, **kwargs):
        token = kwargs["token"]
        command = kwargs["command"]

        # if not helpers.exists("commands", token=token):
        # return {"errors": ["doom and stuff. Probably some death too"]}, 400

        # TODO: Implement cross-platform regex for checking valid tokens.
        # Currently just looking to see if anything exists with that token
        # if not helpers.is_valid_token(token):
        # return {"errors": "doom and stuff. Probably some death too."}, 400

        path_data = {"token": token}

        if command.isdigit():
            path_data["commandId"] = int(command)
            # TODO: Make this get the associated name from the commands table
            #       If it doesn't exist then there will have to be a name key
            #       in the request JSON
            path_data["name"] = "foo"
        else:
            path_data["name"] = command.lower()
            # TODO: Make this get the associated ID from the commands table
            #       OR make it get the next ID from the user table if
            #       the command with the name provided doesn't exist
            path_data["commandId"] = 1

        json_data = request.get_json()

        if json_data is None:
            return {"errors": ["Bro...no data"]}, 400

        data = {**json_data, **path_data}

        response, errors, code = helpers.create_or_update(
            "command", CommandModel, data, ["commandId", "token"]
        )

        return {"data": response, "errors": errors}, code
