from flask import request, make_response, g

from flask_restplus import Resource, marshal

from datetime import datetime

from .. import api
from ..models import Trust
from ..schemas import TrustSchema
from ..util import helpers, auth
from .. import limiter


class TrustList(Resource):
    """
    Lists all the trusts. Has to be defined separately because of how
    Flask-RESTPlus works.
    """

    @limiter.limit("1000/day;90/hour;20/minute")
    @helpers.check_limit
    def get(self, **kwargs):
        attributes, errors, code = helpers.multi_response(
            "trust", Trust, **kwargs)

        response = {}

        if errors != []:
            response["errors"] = errors
        else:
            response["data"] = attributes

        return response, code


class TrustResource(Resource):

    @limiter.limit("1000/day;90/hour;20/minute")
    @auth.scopes_required({"trust:create", "trust:manage"})
    @helpers.lower_kwargs("token", "userId")
    def patch(self, path_data, **kwargs):
        data = {**helpers.get_mixed_args(), **path_data}
        attributes, errors, code = helpers.create_or_update(
            "trust", Trust, data, "token", "userId")

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
    @helpers.lower_kwargs("token")
    def get(self, path_data, **kwargs):
        """
        /api/v1/channel/:token/trust/:trust -> str username
        """
        if kwargs["userId"].isdigit():
            path_data["userId"] = kwargs["userId"]
        else:
            path_data["userName"] = kwargs["userId"]

        attributes, errors, code = helpers.single_response(
            "trust", Trust, **path_data)

        response = {}

        if errors == {}:
            response["data"] = attributes
        else:
            response["errors"] = errors

        return response, code

    @limiter.limit("1000/day;90/hour;20/minute")
    @auth.scopes_required({"trust:manage"})
    @helpers.lower_kwargs("token", "userId")
    def delete(self, path_data, **kwargs):
        deleted = helpers.delete_record("trust", **path_data)

        if deleted is not None:
            return {"meta": {"deleted": deleted}}, 200
        else:
            return None, 404
