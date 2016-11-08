from flask import request, make_response, g

from flask_restplus import Resource, marshal

from datetime import datetime

from .. import api
from ..models import Trust
from ..schemas import TrustSchema
from ..util import helpers


class TrustList(Resource):
    """
    Lists all the trusts. Has to be defined separately because of how
    Flask-RESTPlus works.
    """

    def get(self, **kwargs):
        response, errors, code = helpers.multi_response(
            "trust", Trust, {"token": kwargs["token"]})

        return {"data": response, "errors": errors}, code


class TrustResource(Resource):

    def patch(self, **kwargs):
        path_data = {"token": kwargs["token"], "userName": kwargs["userName"]}
        json_data = request.get_json()

        if json_data is None:
            return {"errors": ["Bro ... no data"]}, 400

        data = {**json_data, **path_data}
        response, errors, code = helpers.create_or_update(
            "trust", Trust, data, ["token", "userName"]
        )

        return {"data": response, "errors": errors}, code

    def get(self, **kwargs):
        """
        /api/v1/channel/:token/trust/:trust -> str username
        """
        # TODO: Implement token validity checking
        path_data = {"token": kwargs["token"], "userName": kwargs["userName"]}

        response, errors, code = helpers.single_response(
            "trust", Trust, path_data
        )

        return {"data": response, "errors": errors}, code

    def delete(self, **kwargs):
        path_data = {"token": kwargs["token"], "userName": kwargs["userName"]}

        deleted = helpers.delete_record("trust", **path_data)

        if deleted is not None:
            return {"meta": {"deleted": deleted}}, 200
        else:
            return None, 404
