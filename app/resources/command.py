from flask import request, make_response, g

from flask_restplus import Resource, marshal, fields, reqparse, fields

from datetime import datetime

from .. import api
from ..models import Command, fields_map
from ..util import helpers
# TODO: Convert all these as resp_helpers, r_helpers, etc. to single helpers
from ..util import resource_helpers as r_helpers

import logging

log = logging.getLogger(__name__)

parser = reqparse.RequestParser()


class CommandList(Resource):
    """
    Lists all the commands. Has to be defined separately because of how
    Flask-RESTPlus works.
    """

    def get(self, **kwargs):
        return helpers.get_multiple("commands")


class CommandResource(Resource):

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

        response = helpers.get_one("commands")

        if len(response) > 0:
            response = response[0]
            return marshal(
                Command(
                    name=response["name"],
                    command_id=response["id"],
                    response=response["response"],
                    # user_id=None,
                    # user_name=None,
                    channel_name=response["channel"],
                    channel_id=response["channelId"],
                    enabled=response["enabled"],
                    deleted=response["deleted"],
                    user_level=response["userLevel"]
                ), Command.model), 200
        else:
            return {"foo": "bar"}, 500

    def patch(self, **kwargs):

        created, code = r_helpers.create("command", Command)

        return created, code

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
