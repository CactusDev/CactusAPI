from flask import request

from flask_restplus import Resource, marshal

from datetime import datetime

from .. import api
from ..models import Social
from ..schemas import SocialSchema
from ..util import helpers


class SocialList(Resource):
    """
    Lists all the trusts. Has to be defined separately because of how
    Flask-RESTPlus works.
    """

    @helpers.lower_kwargs("token")
    def get(self, path_data, **kwargs):
        attributes, errors, code = helpers.multi_response(
            "social", Social, **path_data)

        response = {}

        if errors != []:
            response["errors"] = errors
        else:
            response["data"] = attributes

        return response, code


class SocialResource(Resource):

    @helpers.lower_kwargs("token", "service")
    def patch(self, path_data, **kwargs):
        data = helpers.get_mixed_args()

        if data is None:
            return {"errors": ["No JSON data"]}, 400

        data = {**data, **path_data}
        attributes, errors, code = helpers.create_or_update(
            "social", Social, data, "token", "service"
        )

        response = {}

        if code == 201:
            response["meta"] = {"created": True}
        elif code == 200:
            response["meta"] = {"edited": True}

        if errors == {}:
            response["attributes"] = attributes
        else:
            response["errors"] = errors

        return response, code

    @helpers.lower_kwargs("token", "service")
    def get(self, path_data, **kwargs):
        attributes, errors, code = helpers.single_response(
            "social", Social, **path_data
        )

        response = {}

        if errors == {}:
            response["data"] = attributes
        else:
            response["errors"] = errors

        return response, code

    @helpers.lower_kwargs("token", "service")
    def delete(self, path_data, **kwargs):
        deleted = helpers.delete_record("social", **path_data)

        if deleted is not None:
            return {"meta": {"deleted": deleted}}, 200
        else:
            return None, 404
