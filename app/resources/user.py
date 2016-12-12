"""User resource"""

from flask import request

from flask_restplus import Resource, marshal

from .. import api
from ..models import User
from ..schemas import UserSchema
from ..util import helpers

# TODO: Solve createdAt cannot be formatted as datetime bug


class UserList(Resource):
    """
    Lists all the Users. Has to be defined separately because of how
    Flask-RESTPlus works.
    """

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

    @helpers.lower_kwargs("token")
    def get(self, path_data, **kwargs):
        attributes, errors, code = helpers.single_response(
            "user", User, **path_data)

        response = {}

        if errors == {}:
            response["data"] = attributes
        else:
            response["errors"] = errors

        return response, code

    @helpers.lower_kwargs("token")
    def post(self, path_data, **kwargs):
        json_data = request.get_json()

        if json_data is None:
            return {"errors": ["Bro...no data"]}, 400

        data = {**path_data, **json_data}

        # TODO: Have to check if that token exists already, can't allow
        # duplicates
        attributes, errors, code = helpers.create_or_update(
            "user", User, data, "service", "userId", post=True
        )

        response = {}

        if errors == {}:
            response["data"] = attributes
        else:
            response["errors"] = errors

        return response, code

    @helpers.lower_kwargs("token")
    def delete(self, path_data, **kwargs):
        deleted = helpers.delete_record(
            "user", **path_data)

        if deleted is not None:
            return {"meta": {"deleted": deleted}}, 200
        else:
            return None, 404
