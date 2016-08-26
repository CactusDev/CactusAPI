"""Views for the API"""

# TODO: Make resource creation/editing smarter in terms of required values
# TODO: Auth checking

import time
from datetime import datetime, timedelta
import remodel.connection
import requests
import pytz
import redis
import rethinkdb as rethink
from uuid import uuid4
from flask import jsonify, request, g, make_response
from models import User, Command, Quote, Message, Friend
from helpers import *

from run import app

remodel.connection.pool.configure(db=app.config["RDB_DB"],
                                  host=app.config["RDB_HOST"],
                                  port=app.config["RDB_PORT"])
REDIS_CONN = redis.Redis()

META_CREATED = {
    "created": True,
    "updated": False
}

META_EDITED = {
    "created": False,
    "updated": True
}


@app.before_request
def before_request():
    """Set the Flask session object's user to Flask-Login's current_user"""
    g.rdb_conn = rethink.connect(host=app.config["RDB_HOST"],
                                 port=app.config["RDB_PORT"],
                                 db=app.config["RDB_DB"])


@app.route("/api/v1/channel/<channel>/friend", methods=["GET"])
def chan_friends(channel):
    """
    If you GET this endpoint, go to /api/v1/channel/<channel>/friend
    with <channel> replaced for the channel of the friends you want to get

    <channel> can either be an int that matches the channel, or a string
    that matches the owner's username
    """

    # model = request.path.split("/")[-1]
    model = "Friend"

    if channel.isdigit():
        fields = {"channelId": int(channel)}
    else:
        fields = {"owner": channel.lower()}

    packet, code = generate_response(
        model,
        request.path,
        request.method,
        request.values,
        data=results,
        fields=fields
    )

    return make_response(jsonify(packet), code)

    # There was an error!
    # if not str(code).startswith("2"):
    #    return make_response(jsonify(packet), code)
    # NOTE: Not needed currently, but this is how you would check


# TODO: Fix this endpoint to remove timing elements (friends are forever)
# TODO: Use Object.update(**changes) instead of Object(**updated_object).save()
@app.route("/api/v1/channel/<channel>/friend/<friend>",
           methods=["GET", "POST", "DELETE"])
def chan_friend(channel, friend):
    """
    If you GET this endpoint, go to /api/v1/channel/<channel>/friend/<friend>
    with <channel> replaced for the channel you want and <friend> for the
    the user ID you want to look up.

    If you POST this endpoint:
        Go to /api/v1/channel/<channel>/friend/<friend> with <channel>
        for the channel wanted & <friend> replaced for the user ID of the
        friend you want to edit or create.
    """

    model = "Friend"

    # Get beam data for the provided channel (<channel>)
    data = requests.get(
        "https://beam.pro/api/v1/channels/{}".format(channel)).json()
    channel_id = data["id"]
    token = data["token"]

    # Get beam data for the provided user (<friend>)
    endpoint = "users" if friend.isdigit() else "channels"
    # If it's numeric, "users" endpoint, else "channels"

    data = requests.get(
        "https://beam.pro/api/v1/{}/{}".format(
            endpoint, friend
        ), params={"limit": 1}
    ).json()

    if len(data) > 1:
        if "user" in data:
            data = data["user"]

        user_id = data["id"]
        username = data["username"]
    else:
        # Error handling for getting data
        print("Errors and weirdness!")
        print("data:\t", data)

    data = {
        "channelId": channel_id,
        "token": token,
        "userName": username,
        "userId": user_id
    }

    response = generate_response(
        model,
        request.path,
        request.method,
        request.values,
        user=username,
        data=data
    )

    return make_response(jsonify(response[0]), response[1])


@app.route("/api/v1/channel/<channel>/message", methods=["GET"])
def chan_messages(channel):

    """
    If you GET this endpoint, go to /api/v1/channel/<channel>/messages
    with <channel> replaced for the messages you want to get
    """

    model = "Message"

    if channel.isdigit():
        fields = {"channelId": int(channel)}
    else:
        fields = {"owner": channel.lower()}

    packet, code = generate_response(
        model,
        request.path,
        request.method,
        request.values,
        fields=fields
    )

    return make_response(jsonify(packet), code)


@app.route("/api/v1/channel/<channel>/message/<message>",
           methods=["GET", "POST", "DELETE"])
def chan_message(channel, message):
    """
    If you GET this endpoint, go to /api/v1/channel/<channel>/message/<message>
    with <channel> replaced for the channel you want and <message> for the
    the message ID you want to look up. Will return the raw packet for the
    message as well, unlike /channel/<channel>/message

    If you POST this endpoint:
        Go to /api/v1/channel/<channel>/message/<message> with <channel>
        for the channel wanted & <message> replaced for the ID of the message
        you want to edit or create

        Parameters:
            - message:      Raw message contents in string
            - timestamp:    A Unix-epoch int of when the message was sent
            - userId:       The user ID who sent the message
            - packet:       The raw JSON packet in string form from Beam
    """

    model = "Message"
    errors = []

    required_parameters = ["message", "timestamp", "userId", "packet"]

    for param in request.values:
        if param not in required_parameters:
            errors.append(
                generate_error(
                    uid=uuid4(),
                    status="400",
                    title="Incorrect parameters for endpoint",
                    detail="Missing required {} parameter".format(param),
                    source={"pointer": request.path}
                )
            )

    channel = int(channel) if channel.isdigit() else channel

    fields = {"channelId": channel, "messageId": message}

    data = {
        key: request.values.get(key) for key in request.values
    }
    data.update(**fields)
    data.update({
        "createdAt": rethink.epoch_time(
            int(request.values.get("timestamp", time.time()))
        )
    })

    data = {key: unescape(data[key]) for key in data
            if isinstance(data[key], str)}

    response = generate_response(
        model,
        request.path,
        request.method,
        request.values,
        data=data,
        fields=fields
    )

    packet = response[0]

    return make_response(jsonify(response[0]), response[1])


@app.route("/api/v1/channel/<channel>/quote", methods=["GET"])
def user_quotes(channel):
    """
    If you GET this endpoint, go to /api/v1/channel/<channel>/quote
    with <channel> replaced for the channel you want to get quotes for
    """
    model = "quote"

    if channel.isdigit():
        fields = {"channelId": int(channel), "deleted": False}
    else:
        fields = {"owner": channel.lower(), "deleted": False}

    packet, code = generate_response(
        model,
        request.path,
        request.method,
        request.values,
        fields=fields
    )

    return make_response(jsonify(packet), code)


@app.route("/api/v1/channel/<channel>/quote/<int:quoteId>",
           methods=["GET", "PATCH", "DELETE"])
def chan_quote(channel, quoteId):
    """
    If you GET this endpoint:
        Go to /api/v1/channel/<channel>/quote/<quote> with <channel> replaced
        for the channel you want and <quote> replaced with the quote ID you
        wish to look up

    If you PATCH this endpoint:
        Go to /api/v1/channel/<channel>/quote/<quote> with <channel> replaced
        for the channel wanted & <quote> replaced for the ID of the quote you
        want to look up

        Parameters needed:
            - quote:        The new contents of the quote
            - messageId:    The ID of the quote's message
            - userId:       The ID of the message's sender

    If you DELETE this endpoint:
        Go to /api/v1/channel/<channel>/quote/<quote> with <channel> replaced
        for the channel you want and <quote> replaced with the quote ID you
        want to remove
    """
    model = "Quote"

    channel = int(channel) if channel.isdigit() else channel

    fields = {
        "channelId": channel,
        "quoteId": quoteId
    }

    data = {
        key: request.values.get(key) for key in request.values
    }
    data.update(**fields)

    for key in data:
        if isinstance(data[key], str):
            data[key] = unescape(data[key])

    data = {key: data[key] for key in data if data[key] is not None}

    response = generate_response(
        model,
        request.path,
        request.method,
        request.values,
        data=data,
        fields=fields
    )

    packet = response[0]

    return make_response(jsonify(response[0]), response[1])


@app.route("/api/v1/user/<string:username>",
           methods=["GET", "PATCH", "DELETE"])
def beam_user(username):

    """
    If you GET this endpoint, simply go to /api/v1/user/<username> with
    <username> replaced for the user you want

    If you PATCH this endpoint:
        Go to /api/v1/user/<username> with <username> replaced for the user
            wanted
        Parameters needed:
            - email:    User's email address
            - provider: OAuth provider
            - pid:      User ID from OAuth provider
    """
    model = "User"

    fields = {"channelId": channel,
              "quoteId": quote}

    data = {
        "email": request.values.get("email"),
        "providerId": "{}${}".format(request.values.get("provider", ""),
                                     request.values.get("pid", "")),
        "roles": ["user"],
        "userName": username
    }

    for key in data:
        if isinstance(data[key], str):
            data[key] = unescape(data[key])

    data = {key: data[key] for key in data if data[key] is not None}

    response = generate_response(
        model,
        request.path,
        request.method,
        request.values,
        data=data,
        fields=fields
    )

    packet = response[0]

    return make_response(jsonify(response[0]), response[1])


@app.route("/api/v1/channel/<channel>/command", methods=["GET"])
def user_commands(channel):

    """
    If you GET this endpoint, simply go to /api/v1/channel/<channel>/command
    with <channel> replaced for the channel you want to get commands for
    """
    model = "Command"

    if channel.isdigit():
        fields = {"channelId": int(channel), "deleted": False}
    else:
        fields = {"channelName": channel.lower(), "deleted": False}

    packet, code = generate_response(
        model,
        request.path,
        request.method,
        request.values,
        fields=fields
    )

    return make_response(jsonify(packet), code)


@app.route("/api/v1/channel/<channel>/command/<int:cmd>",
           methods=["GET", "PATCH", "DELETE"])
def user_command(channel, cmd):
    """
    If you GET this endpoint, go to /api/v1/channel/<channel>/command/<cmd>
    with <channel> replaced for the channel you want & <cmd> replaced with the
    command you wish to look up

    If you PATCH this endpoint:
        Go to /api/v1/channel/<channel>/command/<cmd> with <channel> replaced
            for the channel wanted & <cmd> replaced with the command you wish
            to look up or the command ID
    """

    model = "Command"

    if channel.isdigit():
        fields = {"channelId": int(channel), "commandId": cmd}
    else:
        fields = {"channelName": channel.lower(), "commandId": cmd}

    data = dict(request.values)

    data = {
        key: request.values.get(key) for key in request.values
    }
    data.update(**fields)

    for key in data:
        if isinstance(data[key], str):
            data[key] = unescape(data[key])

    data = {key: data[key] for key in data if data[key] is not None}

    response = generate_response(
        model,
        request.path,
        request.method,
        request.values,
        data=data,
        fields=fields
    )

    packet = response[0]

    return make_response(jsonify(response[0]), response[1])
