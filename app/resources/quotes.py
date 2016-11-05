from flask import request, make_response, g

from flask_restplus import Resource, marshal

from datetime import datetime

from .. import api
from ..models import Quote
from ..schemas import QuoteSchema
from ..util import helpers


class QuoteList(Resource):
    """
    Lists all the quotes. Has to be defined separately because of how
    Flask-RESTPlus works.
    """

    def get(self, **kwargs):
        response, errors, code = helpers.multi_response(
            "quote", Quote, {"token": kwargs["token"]})

        return {"data": response, "errors": errors}, code


class QuoteResource(Resource):

    def patch(self, **kwargs):
        # TODO: Implement trust creation/editing
        pass

    def get(self, **kwargs):
        return Quote.schema.load({**request.get_json(), **kwargs}), 200

    def delete(self, **kwargs):
        # TODO: Implement DELETE functionality
        pass

#
# @app.route("/api/v1/channel/<channel>/quote", methods=["GET"])
# def user_quotes(channel):
#     """
#     If you GET this endpoint, go to /api/v1/channel/<channel>/quote
#     with <channel> replaced for the channel you want to get quotes for
#     """
#     model = "quote"
#
#     if channel.isdigit():
#         fields = {"channelId": int(channel), "deleted": False}
#     else:
#         fields = {"owner": channel.lower(), "deleted": False}
#
#     packet, code = generate_response(
#         model,
#         request.path,
#         request.method,
#         request.values,
#         fields=fields
#     )
#
#     return make_response(jsonify(packet), code)
#
#
# @app.route("/api/v1/channel/<channel>/quote/<int:quoteId>",
#            methods=["GET", "PATCH", "DELETE"])
# def chan_quote(channel, quoteId):
#     """
#     If you GET this endpoint:
#         Go to /api/v1/channel/<channel>/quote/<quote> with <channel> replaced
#         for the channel you want and <quote> replaced with the quote ID you
#         wish to look up
#
#     If you PATCH this endpoint:
#         Go to /api/v1/channel/<channel>/quote/<quote> with <channel> replaced
#         for the channel wanted & <quote> replaced for the ID of the quote you
#         want to look up
#
#         Parameters needed:
#             - quote:        The new contents of the quote
#             - messageId:    The ID of the quote's message
#             - userId:       The ID of the message's sender
#
#     If you DELETE this endpoint:
#         Go to /api/v1/channel/<channel>/quote/<quote> with <channel> replaced
#         for the channel you want and <quote> replaced with the quote ID you
#         want to remove
#     """
#     model = "Quote"
#
#     channel = int(channel) if channel.isdigit() else channel
#
#     fields = {
#         "channelId": channel,
#         "quoteId": quoteId
#     }
#
#     data = {
#         key: request.values.get(key) for key in request.values
#     }
#     data.update(**fields)
#
#     for key in data:
#         if isinstance(data[key], str):
#             data[key] = unescape(data[key])
#
#     data = {key: data[key] for key in data if data[key] is not None}
#
#     response = generate_response(
#         model,
#         request.path,
#         request.method,
#         request.values,
#         data=data,
#         fields=fields
#     )
#
#     packet = response[0]
#
#     return make_response(jsonify(response[0]), response[1])
