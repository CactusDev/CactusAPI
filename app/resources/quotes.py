"""Handles all of the API endpoints related to quotes"""

from flask import request

from flask_restplus import Resource, marshal

from .. import api
from ..models import Quote
from ..schemas import QuoteSchema
from ..util import helpers
from .. import limiter


class QuoteList(Resource):
    """
    Lists all the quotes. Has to be defined separately because of how
    Flask-RESTPlus works.
    """

    @limiter.limit("1000/day;90/hour;20/minute")
    @helpers.check_random
    @helpers.check_limit
    @helpers.lower_kwargs("token")
    def get(self, path_data, **kwargs):
        data = {**helpers.get_mixed_args(), **path_data}
        attributes, errors, code = helpers.multi_response(
            "quote", Quote, **data
        )

        response = {}

        if errors != []:
            response["errors"] = errors
        else:
            response["data"] = attributes

        return response, code

    @limiter.limit("1000/day;90/hour;20/minute")
    @helpers.lower_kwargs("token")
    def post(self, path_data, **kwargs):
        data = helpers.get_mixed_args()

        # TODO: Make this an actual error/let Marshmallow handle it
        if data is None:
            return {"errors": ["Bro ... no data"]}, 400

        data = {**data,
                **path_data,
                "quoteId": helpers.next_numeric_id(
                    "quote",
                    id_field="quoteId",
                    **path_data
                )}

        attributes, errors, code = helpers.create_or_update(
            "quote", Quote, data, "quote", "token", post=True)

        response = {}

        if errors != {}:
            response["errors"] = errors
        else:
            response["data"] = attributes

        return response, code


class QuoteResource(Resource):

    @limiter.limit("1000/day;90/hour;20/minute")
    @helpers.lower_kwargs("token", "quoteId")
    def patch(self, path_data, **kwargs):
        """Create or edit a quote resource"""
        data = helpers.get_mixed_args()

        # TODO: Make this an actual error/let Marshmallow handle it
        if data is None:
            return {"errors": ["Bro ... no data"]}, 400

        data = {**data, **path_data}
        attributes, errors, code = helpers.create_or_update(
            "quote", Quote, data, "token", "quoteId"
        )

        response = {}

        if code == 201:
            response["meta"] = {"created": True}
        elif code == 200:
            response["meta"] = {"edited": True}

        if errors != {}:
            response["errors"] = errors
        else:
            response["data"] = attributes

        return response, code

    @limiter.limit("1000/day;90/hour;20/minute")
    @helpers.lower_kwargs("token", "quoteId")
    def get(self, path_data, **kwargs):
        """Get a single quote"""
        attributes, errors, code = helpers.single_response(
            "quote", Quote, **path_data
        )

        response = {}

        if errors == {}:
            response["data"] = attributes
        else:
            response["errors"] = errors

        return response, code

    @helpers.lower_kwargs("token", "quoteId")
    def delete(self, path_data, **kwargs):
        """Delete a quote resource"""
        deleted = helpers.delete_record("quote", **path_data)

        if deleted is not None:
            return {"meta": {"deleted": deleted}}, 200
        else:
            return None, 404
