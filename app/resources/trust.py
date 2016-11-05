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
        # TODO: Implement trust creation/editing
        pass

    def get(self, **kwargs):
        return Trust.schema.load({**request.get_json(), **kwargs}), 200

    def delete(self, **kwargs):
        # TODO: Implement DELETE functionality
        pass

#
# @app.route("/api/v1/channel/<channel>/friend", methods=["GET"])
# def chan_friends(channel):
#     """
#     If you GET this endpoint, go to /api/v1/channel/<channel>/friend
#     with <channel> replaced for the channel of the friends you want to get
#
#     <channel> can either be an int that matches the channel, or a string
#     that matches the owner's username
#     """
#
#     model = "Friend"
#
#     if channel.isdigit():
#         fields = {"channelId": int(channel)}
#     else:
#         fields = {"owner": channel.lower()}
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
#     # There was an error!
#     # if not str(code).startswith("2"):
#     #    return make_response(jsonify(packet), code)
#     # NOTE: Not needed currently, but this is how you would check
#
#
# # TODO:500 Use Object.update(**changes) instead of
# # Object(**updated_object).save()
# @app.route("/api/v1/channel/<channel>/friend/<friend>",
#            methods=["GET", "POST", "DELETE"])
# @auth.scopes_required(["friend:create", "friend:delete", "friend:edit"])
# def chan_friend(channel, friend):
#     """
#     If you GET this endpoint, go to /api/v1/channel/<channel>/friend/<friend>
#     with <channel> replaced for the channel you want and <friend> for the
#     the user ID you want to look up.
#
#     If you POST this endpoint:
#         Go to /api/v1/channel/<channel>/friend/<friend> with <channel>
#         for the channel wanted & <friend> replaced for the user ID of the
#         friend you want to edit or create.
#     """
#
#     model = "Friend"
#
#     # Get beam data for the provided channel (<channel>)
#     data = requests.get(
#         "https://beam.pro/api/v1/channels/{}".format(channel)).json()
#     channel_id = data["id"]
#     token = data["token"]
#
#     # Get beam data for the provided user (<friend>)
#     endpoint = "users" if friend.isdigit() else "channels"
#     # If it's numeric, "users" endpoint, else "channels"
#
#     data = requests.get(
#         "https://beam.pro/api/v1/{}/{}".format(
#             endpoint, friend
#         ), params={"limit": 1}
#     ).json()
#
#     if len(data) > 1:
#         if "user" in data:
#             data = data["user"]
#
#         user_id = data["id"]
#         username = data["username"]
#     else:
#         # Error handling for getting data
#         print("Errors and weirdness!")
#         print("data:\t", data)
#
#     data = {
#         "channelId": channel_id,
#         "token": token,
#         "userName": username,
#         "userId": user_id
#     }
#
#     response = generate_response(
#         model,
#         request.path,
#         request.method,
#         request.values,
#         user=username,
#         data=data
#     )
#
#     return make_response(jsonify(response[0]), response[1])
