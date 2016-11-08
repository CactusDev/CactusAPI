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
        response, errors, code = helpers.multi_response(
            "quote", Ticket, {"token": kwargs["token"]})

        return {"data": response, "errors": errors}, code


class TicketResource(Resource):

    def patch(self, **kwargs):
        path_data = {"ticketId": kwargs["ticketId"]}

        json_data = request.get_json()

        # TODO: Make this an actual error/let Marshmallow handle it
        if json_data is None:
            return {"errors": ["Bro ... no data"]}, 400

        data = {**json_data, **path_data}
        response, errors, code = helpers.create_or_update(
            "ticket", Ticket, data, ["ticketid"]
        )

        return {"data": response, "errors": errors}, code

    def get(self, **kwargs):
        path_data = {"ticketId": kwargs["ticketId"]}

        response, errors, code = helpers.single_response(
            "ticket", Ticket, path_data
        )

        return {"data": response, "errors": errors}, code

    def delete(self, **kwargs):
        path_data = {"ticketId": kwargs["ticketId"]}

        deleted = helpers.delete_record("ticket", **path_data)

        if deleted is not None:
            return {"meta": {"deleted": deleted}}, 200
        else:
            return None, 404
