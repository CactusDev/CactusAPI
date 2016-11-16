from flask import request, make_response, g

from flask_restplus import Resource, marshal

from datetime import datetime

from .. import api
from ..models import Ticket
from ..schemas import TicketSchema
from ..util import helpers


class TicketList(Resource):
    """
    Lists all the quotes. Has to be defined separately because of how
    Flask-RESTPlus works.
    """

    def get(self, **kwargs):
        attributes, errors, code = helpers.multi_response(
            "quote", Ticket, {"token": kwargs["token"]})

        response = {}

        if errors == {}:
            response["data"] = attributes
        else:
            response["errors"] = errors

        return response, code


class TicketResource(Resource):

    def patch(self, **kwargs):
        path_data = {"ticketId": kwargs["ticketId"]}

        json_data = request.get_json()

        # TODO: Make this an actual error/let Marshmallow handle it
        if json_data is None:
            return {"errors": ["Bro ... no data"]}, 400

        data = {**json_data, **path_data}
        attributes, errors, code = helpers.create_or_update(
            "ticket", Ticket, data, ["ticketId"]
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

    def get(self, **kwargs):
        path_data = {"ticketId": kwargs["ticketId"]}

        attributes, errors, code = helpers.single_response(
            "ticket", Ticket, path_data
        )

        response = {}

        if errors == {}:
            response["data"] = attributes
        else:
            response["errors"] = errors

        return response, code

    def delete(self, **kwargs):
        path_data = {"ticketId": kwargs["ticketId"]}

        deleted = helpers.delete_record("ticket", **path_data)

        if deleted is not None:
            return {"meta": {"deleted": deleted}}, 200
        else:
            return None, 404
