from flask import request

from flask_restplus import Resource, abort, fields, reqparse

from .. import api
from ..models import Command
from ..util.helpers import *

import logging

parser = reqparse.RequestParser()

log = logging.getLogger(__name__)


class CommandList(Resource):
    """
    Lists all the commands. Has to be defined separately because of how
    Flask-RESTPlus works.
    """

    def get(self, **kwargs):
        return get_multiple("commands")


class CommandResource(Resource):

    @api.marshal_with(Command.model)
    def get(self, **kwargs):
        """
        If you GET this endpoint, go to /api/v1/channel/<channel>/command
        with <channel> replaced for the channel you want to get commands for
        """
        channel = kwargs["channel"]

        if channel.isdigit():
            fields = {"channelId": int(channel), "deleted": False}
        else:
            fields = {"channelName": channel.lower(), "deleted": False}

        response = get_one("commands")

        if len(response) > 0:
            response = response[0]
            return Command(
                name=response["name"],
                command_id=response["id"],
                response=response["response"],
                user_id=None,
                user_name=None,
                channel_name=response["channel"],
                channel_id=response["channelId"],
                enabled=response["enabled"],
                deleted=response["deleted"],
                user_level=response["userLevel"]
            )
        else:
            abort(500, "foo", custom="bar", spam="eggs")

        # Custom errors if needed, otherwise abort() does a prebuilt 500
        # abort(CODE_INT, CUSTOM_MSG, CUSTOM_KEY=CUSTOM_TEXT)

    def post(self):
        return {"spam": "eggs"}

#
# @app.route("/api/v1/channel/<channel>/command", methods=["GET"])
# def user_commands(channel):
#

#
#
# @app.route("/api/v1/channel/<channel>/command/<int:cmd>",
#            methods=["GET", "PATCH", "DELETE"])
# def user_command(channel, cmd):
#     """
#     If you GET this endpoint, go to /api/v1/channel/<channel>/command/<cmd>
#     with <channel> replaced for the channel you want & <cmd> replaced with the
#     command you wish to look up
#
#     If you PATCH this endpoint:
#         Go to /api/v1/channel/<channel>/command/<cmd> with <channel> replaced
#             for the channel wanted & <cmd> replaced with the command you wish
#             to look up or the command ID
#     """
#
#     model = "Command"
#
#     if channel.isdigit():
#         fields = {"channelId": int(channel), "commandId": cmd}
#     else:
#         fields = {"channelName": channel.lower(), "commandId": cmd}
#
#     data = dict(request.values)
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
