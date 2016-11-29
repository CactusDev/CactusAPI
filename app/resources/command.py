"""Command resource"""

from flask import request

from flask_restplus import Resource, marshal

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
        attributes, errors, code = helpers.multi_response(
            "command", Command, **{"token": kwargs["token"].lower()})

        response = {}

        if errors != []:
            response["errors"] = errors
        else:
            response["data"] = attributes

        return response, code


class CommandResource(Resource):
    # TODO: Move repetitive kwargs parsing into function/decorator

    @helpers.lower_kwargs(["token", "name"])
    def get(self, **kwargs):
        """/api/v1/:token/command/:command -> [str Command name]"""
        # TODO:210 Implement cross-platform regex for checking valid tokens.

        attributes, errors, code = helpers.single_response(
            "command", Command, **path_data)

        response = {}

        if errors == {}:
            response["data"] = attributes
        else:
            response["errors"] = errors

        return response, code

    @helpers.lower_kwargs(["token", "name"])
    def patch(self, path_data={}, **kwargs):
        # TODO:220 Implement cross-platform regex for checking valid tokens.

        json_data = request.get_json()

        if json_data is None:
            return {"errors": ["Bro...no data"]}, 400

        data = {**json_data, **path_data}

        attributes, errors, code = helpers.create_or_update(
            "command", Command, data, ["token", "name"]
        )

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

    @helpers.lower_kwargs(["token", "name"])
    def delete(self, path_data={}, **kwargs):
        deleted = helpers.delete_record("command", **data)

        if deleted is not None:
            return {"meta": {"deleted": deleted}}, 200
        else:
            return None, 404
