"""Handles all of the API endpoints related to quotes"""

from flask import request

from flask_restplus import Resource, marshal

from .. import api
from ..models import Quote
from ..schemas import QuoteSchema
from ..util import helpers


class QuoteList(Resource):
    """
    Lists all the quotes. Has to be defined separately because of how
    Flask-RESTPlus works.
    """

    @helpers.check_limit
    def get(self, **kwargs):
        if request.args.get("random", "").lower() in ["true", '1']:
            if "limit" not in kwargs:
                kwargs["limit"] = 1
            attributes, errors, code = helpers.multi_response(
                "quote", Quote, random=True, **kwargs
            )
        else:
            attributes, errors, code = helpers.multi_response(
                "quote", Quote, **kwargs)

        response = {}

        if errors != []:
            response["errors"] = errors
        else:
            response["data"] = attributes

        return response, code

    def post(self, **kwargs):
        path_data = {"token": kwargs["token"]}

        json_data = request.get_json()

        # TODO: Make this an actual error/let Marshmallow handle it
        if json_data is None:
            return {"errors": ["Bro ... no data"]}, 400

        data = {**json_data,
                **path_data,
                "quoteId": helpers.next_numeric_id(
                    "quote",
                    id_field="quoteId",
                    **path_data
                )}

        attributes, errors, code = helpers.create_or_none(
            "quote", Quote, data, ["quote", "token"])

        response = {}

        # TODO: Make this standardized to [] instead of {}
        if errors != {}:
            response["errors"] = errors
        else:
            response["data"] = attributes

        return response, code


class QuoteResource(Resource):

    def patch(self, **kwargs):
        path_data = {"token": kwargs["token"], "quoteId": kwargs["quoteId"]}

        json_data = request.get_json()

        # TODO: Make this an actual error/let Marshmallow handle it
        if json_data is None:
            return {"errors": ["Bro ... no data"]}, 400

        data = {**json_data, **path_data}
        attributes, errors, code = helpers.create_or_update(
            "quote", Quote, data, ["token", "quoteId"]
        )

        response = {}

        if code == 201:
            response["meta"] = {"created": True}
        elif code == 200:
            response["meta"] = {"edited": True}

        # TODO: Make this standardized to [] instead of {}
        if errors != {}:
            response["errors"] = errors
        else:
            response["data"] = attributes

        return response, code

    def get(self, **kwargs):
        path_data = {"token": kwargs["token"], "quoteId": kwargs["quoteId"]}

        attributes, errors, code = helpers.single_response(
            "quote", Quote, path_data
        )

        response = {}

        # TODO: Make this standardized to [] instead of {}
        if errors == {}:
            response["data"] = attributes
        else:
            response["errors"] = errors

        return response, code

    def delete(self, **kwargs):
        path_data = {"token": kwargs["token"], "quoteId": kwargs["quoteId"]}

        deleted = helpers.delete_record("quote", **path_data)

        if deleted is not None:
            return {"meta": {"deleted": deleted}}, 200
        else:
            return None, 404
