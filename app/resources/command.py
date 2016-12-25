"""Command resource"""

from flask import request

from flask_restplus import Resource

from .. import api
from ..models import Command, User
from ..schemas import CommandSchema
from ..util import helpers, auth
from .. import limiter


class CommandCounter(Resource):

    @limiter.limit("1000/day;90/hour;25/minute")
    @helpers.lower_kwargs("token", "name")
    def patch(self, path_data, **kwargs):
        data = helpers.get_mixed_args()

        if data is None:
            return {"errors": ["Bro...no data"]}, 400

        data = {**data, **path_data}

        attributes, errors, code = helpers.single_response(
            "command", Command, **path_data
        )

        if code == 200:
            new_count = data["count"]

            if not isinstance(new_count, str):
                return {"errors": ["Not a string fool"]}, 400

            count = attributes["attributes"]["count"]

            if new_count[0] == '+' and new_count[1:].isdigit():
                count = count + int(new_count[1:])
            elif new_count[0] == '-' and new_count[1:].isdigit():
                count = count - int(new_count[1:])
            elif new_count[0] == '=' and new_count[1:].isdigit():
                count = int(new_count[1:])

            response = helpers.update_record(
                "commands", {"id": attributes["id"], "count": count})

            if response is not None:
                attributes = response

        response = {}

        if errors == {}:
            response["data"] = attributes
        else:
            response["errors"] = errors

        return response, code


class CommandList(Resource):
    """
    Lists all the commands. Has to be defined separately because of how
    Flask-RESTPlus works.
    """

    @limiter.limit("1000/day;90/hour;20/minute")
    @helpers.check_limit
    @helpers.lower_kwargs("token")
    def get(self, path_data, **kwargs):
        attributes, errors, code = helpers.multi_response(
            "command", Command, **path_data)

        # Handle builtins
        custom_exists = set(obj.get("attributes", {}).get("name")
                            for obj in attributes)

        builtins, errors, code = helpers.multi_response(
            "builtins", Command, **path_data
        )

        for builtin in builtins:
            b_name = builtin.get("attributes", {}).get("name")
            if b_name not in custom_exists:
                attributes.append(builtin)

        response = {}

        if errors != []:
            response["errors"] = errors
        else:
            response["data"] = attributes

        return response, code


class CommandResource(Resource):

    @limiter.limit("1000/day;90/hour;20/minute")
    @helpers.lower_kwargs("token", "name")
    def get(self, path_data, **kwargs):
        """/api/v1/:token/command/:command -> [str Command name]"""

        attributes, errors, code = helpers.single_response(
            "command", Command, **path_data)

        if code == 404:
            attributes, errors, code = helpers.single_response(
                "builtins", Command, **path_data
            )

        response = {}

        if errors == {}:
            response["data"] = attributes
        else:
            response["errors"] = errors

        return response, code

    @limiter.limit("1000/day;90/hour;20/minute")
    @auth.scopes_required({"command:details", "command:create"})
    @helpers.lower_kwargs("token", "name")
    def patch(self, path_data, **kwargs):
        data = helpers.get_mixed_args()

        if data is None:
            return {"errors": ["Bro...no data"]}, 400

        data = {**data, **path_data}

        attributes, errors, code = helpers.create_or_update(
            "command", Command, data, "token", "name"
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

    @limiter.limit("1000/day;90/hour;20/minute")
    @helpers.lower_kwargs("token", "name")
    def delete(self, path_data, **kwargs):
        deleted = helpers.delete_record("command", **path_data)

        if deleted is not None:
            aliases = helpers.delete_record("aliases",
                                            limit=None,
                                            token=path_data["token"],
                                            command=deleted[0]
                                            )

            repeats = helpers.delete_record("repeats",
                                            limit=None,
                                            token=path_data["token"],
                                            command=deleted[0])

            deleted = {"command": deleted,
                       "aliases": aliases, "repeats": repeats}

        if deleted is not None:
            return {"meta": {"deleted": deleted}}, 200
        else:
            return None, 404
