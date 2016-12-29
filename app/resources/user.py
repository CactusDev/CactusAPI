"""User resource"""

from flask import request

from flask_restplus import Resource, marshal

from .. import api
from ..models import User, Config
from ..schemas import UserSchema
from ..util import helpers, auth
from ..util.auth import argon_hash
from .. import limiter


class UserList(Resource):
    """
    Lists all the Users. Has to be defined separately because of how
    Flask-RESTPlus works.

    NOT CURRENTLY ACTIVE
    """

    @limiter.limit("1000/day;90/hour;20/minute")
    def get(self, **kwargs):
        attributes, errors, code = helpers.multi_response(
            "user", User)

        response = {}

        if errors != []:
            response["errors"] = errors
        else:
            response["data"] = attributes

        return response, code


class UserResource(Resource):

    @limiter.limit("1000/day;90/hour;20/minute")
    def get(self, **kwargs):
        # Not using lower_kwargs because we have to assign it to diff. key
        path_data = {"token": kwargs["userName"].lower()}

        attributes, errors, code = helpers.single_response(
            "user", User, **path_data)

        response = {}

        if errors == {}:
            response["data"] = attributes
        else:
            response["errors"] = errors

        return response, code

    @auth.scopes_required({"root"})
    @limiter.limit("1000/day;90/hour;20/minute")
    def post(self, **kwargs):
        """
        Create the new user in the DB and generate the default config
        in the config table
        """
        data = helpers.get_mixed_args()

        if data is None:
            return {"errors": ["Bro...no data"]}, 400

        data = {**data, **kwargs}

        # TODO: Does this need to be changed/improved at all?
        if "password" in data:
            data["password"] = argon_hash(data["password"])

        # TODO: Have to check if that token exists already, can't allow
        # duplicates
        attributes, errors, code = helpers.create_or_update(
            "user", User, data, "service", "userId", post=True
        )

        # Failed creating the user record
        if errors != {}:
            return {"errors": errors}, code

        # Generate the response now, since we don't need to include the config
        response = {}

        if errors == {}:
            response["data"] = attributes
        else:
            response["errors"] = errors

        _, errors, config_code = helpers.create_or_update(
            "config", Config, Config.default_data(data["token"]),
            "token"
        )

        if errors != {}:
            return {"errors": errors}, config_code

        return response, code

    @auth.scopes_required({"root"})
    @limiter.limit("1000/day;90/hour;20/minute")
    def delete(self, **kwargs):
        # Not using lower_kwargs because we have to assign it to diff. key
        deleted = helpers.delete_record(
            "user", token=kwargs["userName"].lower())

        if deleted is not None:
            return {"meta": {"deleted": deleted}}, 200
        else:
            return None, 404
