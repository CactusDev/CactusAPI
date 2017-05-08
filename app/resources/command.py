"""Command resource"""

from flask import request
from flask_restplus import Resource
from collections import OrderedDict

from .. import api
from ..models import Command, User, Alias
from ..schemas import CommandSchema
from ..schemas.helpers import EPOCH_ZERO
from ..util import helpers, auth
from ..util.helpers import APIError
from .. import limiter


class CommandCounter(Resource):

    @limiter.limit("1000/day;90/hour;25/minute")
    @auth.scopes_required({"command:manage"})
    @helpers.catch_api_error
    def patch(self, **kwargs):
        data = {**helpers.get_mixed_args(), "token": kwargs["token"].lower()}

        attributes, errors, code = helpers.single_response(
            "command", Command,
            **{"token": kwargs["token"].lower(), "name": kwargs["name"]}
        )

        if code == 200:
            new_count = data["count"]

            if not isinstance(new_count, str):
                raise APIError({"count": "Must be a string"}, code=400)

            if data.get("id") is not None:
                del data["id"]

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
        data = {**kwargs, **path_data}
        attributes, errors, code = helpers.multi_response(
            "command", Command, **data)

        # Handle builtins
        custom_exists = set(obj.get("attributes", {}).get("name")
                            for obj in attributes)

        builtins, errors, code = helpers.multi_response(
            "builtins", Command, **{key: value for key, value
                                    in data.items() if key != "token"}
        )

        for builtin in builtins:
            b_name = builtin.get("attributes", {}).get("name")
            if b_name not in custom_exists:
                attributes.append(builtin)

        aliases, errors, code = helpers.multi_response(
            "aliases", Alias, **data
        )

        for alias in aliases:
            # HACK: Need to redo this to handle aliases better
            command = helpers.get_one(
                "commands",
                uid=alias["attributes"]["command"]
            )
            del command["name"]

            alias["attributes"].update(command)
            del alias["attributes"]["command"]

        attributes = attributes + aliases

        response = {}

        if errors != []:
            response["errors"] = errors
        else:
            response["data"] = attributes

        return response, code


class CommandResource(Resource):

    @limiter.limit("1000/day;90/hour;20/minute")
    @helpers.lower_kwargs("token")
    def get(self, path_data, **kwargs):
        """/api/v1/:token/command/:command -> [str Command name]"""
        data = {"name": kwargs["name"], **path_data}

        resources = OrderedDict(
            [("command", Command), ("aliases", Alias), ("builtins", Command)])

        for table, model in resources.items():
            if table != "builtins":
                sort_data = data
            else:
                sort_data = {"name": kwargs["name"], "token": "CactusBot"}

            attributes, errors, code = helpers.single_response(
                table, model, cased="name", **sort_data
            )

            # No results were found, go on to the next one
            if code == 404:
                continue

            break

        if attributes.get("type") == "aliases":
            command = helpers.get_one(
                "commands",
                uid=attributes["attributes"]["command"]
            )
            if command != {} and "name" in command:
                del command["name"]

            attributes["attributes"].update(command)
            del attributes["attributes"]["command"]

        response = {}

        if errors == {}:
            response["data"] = attributes
        else:
            response["errors"] = errors

        return response, code

    @limiter.limit("1000/day;90/hour;20/minute")
    @auth.scopes_required({"command:create", "command:manage"})
    @helpers.lower_kwargs("token")
    def patch(self, path_data, **kwargs):
        data = {**helpers.get_mixed_args(),
                "name": kwargs["name"], **path_data}

        if data.get("id") is not None:
            del data["id"]

        attributes, errors, code = helpers.create_or_update(
            "command", Command, data,
            token=kwargs["token"].lower(), name=kwargs["name"],
            cased={"key": "name", "value": kwargs["name"]}
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
    @auth.scopes_required({"command:manage"})
    @helpers.lower_kwargs("token")
    def delete(self, path_data, **kwargs):
        data = {**path_data, "name": kwargs["name"]}

        deleted, code = helpers.delete_soft("commands", **data)

        if code == 200:
            # TODO: Maybe make these actually check for errors by accepting
            # second return object?
            aliases, _ = helpers.delete_soft("aliases",
                                             limit=None,
                                             token=path_data["token"],
                                             command=deleted[0])
            repeats, _ = helpers.delete_soft("repeats",
                                             limit=None,
                                             token=path_data["token"],
                                             command=deleted[0])
            deleted = {
                "command": deleted,
                "aliases": aliases,
                "repeats": repeats
            }
            return {"meta": {"deleted": deleted}}, code
        else:
            return deleted, 404
