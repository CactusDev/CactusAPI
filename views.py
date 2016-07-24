"""Views for the API"""

import rethinkdb as rethink
import remodel.connection
import time
import requests
import pytz
from datetime import datetime, timedelta
from flask import jsonify, request, g, make_response
from models import User, Commands, Quotes, Messages, Friend

from run import APP, make_request

remodel.connection.pool.configure(db=APP.config["RDB_DB"])


META_CREATED = {
    "created": True,
    "updated": False
}

META_EDITED = {
    "created": False,
    "updated": True
}


def retrieve_user(username):
    """Get and return a user."""
    user = rethink.table("users").filter(
        lambda user:
        user["userName"].match("(?i){}".format(str(username)))
    ).limit(1).run(g.rdb_conn)

    return list(user)


def retrieve_single(item, table):
    """ Get and return a single object from the given table via the UUID

    Parameters:
        item:   String of the object's UUID
        table:  String of the table the object is in
    """
    obj = rethink.table(str(table)).filter(
        id=item
    ).limit(1).run(g.rdb_conn)

    return list(obj)


def generate_packet(packet_type, uid, attributes, path, meta=None):
    """Create and return a packet.

    Parameters:
        packet_type:    String of object type being returned
        uid:            ID of whatever is being returned
        attributes:     Dict of data attributes to return
                            MUST include a "user" key
        path:           String of endpoint being accessed for link generation
        meta:           Dict of meta information, not required
    """

    user = attributes.pop("userName") if "userName" in attributes else None

    print("id:\t", uid)
    print("\ttype:\t", packet_type)
    print("\tattr:\t", attributes)
    print("\tpath:\t", path)
    print("\tuser:\t", user)

    relationships = ["command", "quote", "user", "message", "friend"]

    link_base = "/api/v1/user/{}".format(user)

    # TODO: Add code that creates relationships for messages/channel-level

    relationship_return = {key: {
        "links": {
            "self": "{}/relationships/{}".format(link_base, str(key)),
            "related": "{}/{}".format(link_base, str(key))
        }
    } for key in relationships if key != str(packet_type) and user is not None}

    to_return = {
        "data": {
            "type": str(packet_type),
            "id": str(uid),
            "attributes": attributes,
            "relationships": relationship_return,
            "jsonapi": {
                "version": "1.0"
            },
            "links": {
                "self": str(path)
            }
        }
    }

    if meta is not None and isinstance(meta, dict):
        to_return["meta"] = meta

    return to_return


@APP.before_request
def before_request():
    """Set the Flask session object's user to Flask-Login's current_user"""
    g.rdb_conn = rethink.connect(host=APP.config["RDB_HOST"],
                                 port=APP.config["RDB_PORT"],
                                 db=APP.config["RDB_DB"])


@APP.route("/api/v1/channel/<string:channel>/friend", methods=["GET"])
def chan_friends(channel):
    """
    If you GET this endpoint, go to /api/v1/channel/<channel>/friend
    with <channel> replaced for the channel of the friends you want to get
    """
    results = list(
        rethink.table("friends").filter(
            {
                "channelId": channel
            }
        ).run(g.rdb_conn))

    to_return = [generate_packet(
        "friend",
        result["id"],
        {
            "userName": result["userName"],
            "userId": result["userId"],
            "active": result["active"],
            "expiresAt": result["expires"]
        }
    )]

    return jsonify(to_return)


@APP.route("/api/v1/channel/<int:channel>/friend/<int:friend>",
           methods=["GET", "PATCH", "DELETE"])
def chan_friend(channel, friend):
    """
    If you GET this endpoint, go to /api/v1/channel/<channel>/friend/<friend>
    with <channel> replaced for the channel you want and <friend> for the
    the user ID you want to look up.

    If you POST this endpoint:
        Go to /api/v1/channel/<channel>/friend/<friend> with <channel>
        for the channel wanted & <friend> replaced for the user ID of the
        friend you want to edit or create

        Parameters:
            - length:       The number of seconds the friend is going to last
                                Do not include if the friend is permanent
    """
    # Initialize length to 0 now to prevent a NameError from happening later
    length = 0
    # Initialize meta as None now so we don't have to do it multiple time later
    meta = None

    # Pre-create the query
    friend_query = rethink.table("friends").filter(
            {
                "channelId": channel,
                "userId": friend
            }
        )

    if request.method == "GET":

        results = list(friend_query.limit(1).run(g.rdb_conn))

    elif request.method == "PATCH":

        results = list(friend_query.run(g.rdb_conn))

        # It's [] (empty), so we need to make a NEW friend object
        if results == []:

            user = requests.get(
                "https://beam.pro/api/v1/users/{}".format(friend)).json()

            length = int(request.values.get("length", 0))

            # Create the new friend record
            result = Friend(
                channelId=channel,
                userName=user["username"],
                userId=user["id"],
                active=True,
                expires=rethink.epoch_time(
                            int(time.time()) + length
                        ) if length != 0 else rethink.epoch_time(0)
            )

            # and save it
            result.save()

            results = friend_query.limit(1).run(g.rdb_conn)
            # A new friend record was created, so set that meta
            meta = META_CREATED

        else:
            # Get the first result, only want to edit one
            result = results[0]
            # Get length seperately so it's easier to reference
            length = float(request.values.get("length", 0))

            if length != 0:
                # Take the current UTC datetime and then add the # of seconds
                #   .replace is required to make the datetime timezone aware
                #   which is required for RethinkDB
                result["expires"] = (
                    datetime.utcnow() + timedelta(0, length)).replace(
                        tzinfo=pytz.UTC
                    )
            else:
                # Set it to start of all time to signify permanent friend
                result["expires"] = rethink.epoch_time(0)

            # Save the changes
            Friend(
                **result
            ).save()

            results = friend_query.limit(1).run(g.rdb_conn)

            # The friend record was edited, so set that meta
            meta = META_EDITED

        if result["expires"] != rethink.epoch_time(0) and \
                result["expires"] > rethink.epoch_time(time.time()):
            active = True
        else:
            active = False

        if result["expires"] != rethink.epoch_time(0):
            expires = result["expires"]
        else:
            expires = None

        to_return = [generate_packet(
            "friend",
            result["id"],
            {
                "channelId": result["channelId"],
                "userName": result["userName"],
                "userId": result["userId"],
                "active": active,
                "expiresAt": result["expires"]
            },
            request.path,
            meta) for result in results]

    elif request.method == "DELETE":

        results = list(friend_query.limit(1).run(g.rdb_conn))

        # If the user DOES exist in the DB in the friend table
        if results != []:
            try:
                rethink.table("friends").get(
                    results[0]["id"]).delete().run(g.rdb_conn)

                return make_response(jsonify([]), 204)

            except Exception as error:
                print("Exception caught! views:225")
                print(error)

                return make_response(jsonify([{"error": error}]), 500)

    return jsonify(to_return)


@APP.route("/api/v1/channel/<string:channel>/message", methods=["GET"])
def chan_messages(channel):

    """
    If you GET this endpoint, go to /api/v1/channel/<channel>/messages
    with <channel> replaced for the messages you want to get
    """

    results = list(
        rethink.table("messages").filter(
            {
                "channelId": channel
            }
        ).run(g.rdb_conn))

    to_return = [generate_packet(
        "message",
        result["id"],
        {
            "message": result["message"],
            "channelId": channel,
            "userId": result["userId"],
            "createdAt": result["createdAt"]
        }
    )]

    return jsonify(to_return)


@APP.route("/api/v1/channel/<string:channel>/message/<message>",
           methods=["GET", "POST"])
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

    if request.method == "GET":
        results = list(
            rethink.table("messages").filter(
                {
                    "channelId": channel,
                    "id": message
                }
            ).limit(1).run(g.rdb_conn)
        )

        to_return = [generate_packet(
            "message",
            result["id"],
            {
                "message": result["message"],
                "channelId": channel,
                "userId": result["userId"],
                "createdAt": result["createdAt"],
                "packet": result["packet"]
            },
            request.path) for result in results]

    elif request.method == "POST":

        results = list(
            rethink.table("messages").filter(
                {
                    "channelId": channel,
                    "id": message
                }
            ).run(g.rdb_conn)
        )

        # It's [] (empty), so we need to make a NEW quote
        if results == []:
            result = Messages(
                message=request.values.get("message", ""),
                channelId=request.values.get("channelId", ""),
                userId=request.values.get("userId", ""),
                createdAt=rethink.epoch_time(
                    int(request.values.get("timestamp", ""))),
                packet=request.values.get("packet", "")
            )

            result.save()

            results.append(result)

        to_return = [generate_packet(
            "message",
            result["id"],
            {
                "message": result["message"],
                "channelId": channel,
                "userId": result["userId"],
                "createdAt": result["createdAt"],
                "packet": result["packet"]
            },
            request.path,
            {
                "created": True
            }) for result in results]

    return jsonify(to_return)


@APP.route("/api/v1/user/<string:username>/quote", methods=["GET"])
def user_quotes(username):
    """
    If you GET this endpoint, go to /api/v1/user/<username>/quote
    with <username> replaced for the user you want to get quotes for
    """

    # Get all users that match the username
    users = retrieve_user(username)

    # Were any returned?
    if len(users) < 1:
        # No, return 204 since it's not an error, the user just doesn't exist
        return "", 204
    else:
        # Yes, user the first user
        user = users[0]

    results = list(
        rethink.table("quotes").filter(
            {
                "userId": user["id"],
                "deleted": False
            }
        ).run(g.rdb_conn))

    to_return = [generate_packet(
        "quote",
        result["id"],
        {
            "quote": str(result["quote"]),
            "enabled": result["enabled"],
            "channelId": result["channelId"],
            "createdAt": str(result["createdAt"]),
            "messageId": str(result["messageId"]),
            "userId": result["userId"],
            "userName": user["userName"]
        },
        request.path) for result in results]

    return jsonify(to_return)


@APP.route("/api/v1/user/<string:username>/quote/<string:quote>",
           methods=["GET", "PATCH"])
def user_quote(username, quote):
    """
    If you GET this endpoint, go to /api/v1/user/<username>/quote/<quote> with
    <username> replaced for the user you want & <quote> replaced with the quote
    ID you wish to look up

    If you PATCH this endpoint:
        Go to /api/v1/user/<username>/quote/<quote> with <username> replaced
        for the user wanted & <quote> replaced for the ID of the quote you
        want to look up
        Parameters needed:
            - quote: The new contents of the quote
    """

    # Get all users that match the username
    users = retrieve_user(username)

    # Were any returned?
    if len(users) < 1:
        # No, return 204 since it's not an error, the user just doesn't exist
        return "", 204
    else:
        # Yes, user the first user
        user = users[0]

    if request.method == "GET":
        results = list(rethink.table("quotes").filter(
            {"userId": user["id"],
             "id": str(quote)}
        ).limit(1).run(g.rdb_conn))

        to_return = [generate_packet(
            "quote",
            result["id"],
            {
                "quote": str(result["quote"]),
                "enabled": result["enabled"],
                "channelId": result["channelId"],
                "createdAt": str(result["createdAt"]),
                "messageId": str(result["messageId"]),
                "userId": result["userId"],
                "userName": user["userName"]    # For packet generation
            },
            request.path) for result in results]

    elif request.method == "PATCH":

        results = list(
            rethink.table("commands").filter(
                {
                    "userId": user["id"],
                    "id": str(quote)
                }
            ).run(g.rdb_conn)
        )

        # It's [] (empty), so we need to make a NEW quote
        if results == []:
            result = Quotes(
                quote=request.values.get("quote", ""),
                messageId=request.values.get("messageId", ""),
                channelId=request.values.get("channelId", ""),
                createdAt=rethink.now(),
                userId=user["id"],
                enabled=True,
                deleted=False
            )

            result.save()

            to_return = generate_packet(
                "quote",
                result["id"],
                {
                    "quote": str(result["quote"]),
                    "enabled": result["enabled"],
                    "channelId": result["channelId"],
                    "createdAt": str(result["createdAt"]),
                    "messageId": str(result["messageId"]),
                    "userId": result["userId"],
                    "userName": user["userName"]    # For packet generation
                },
                request.path,
                META_CREATED)

        # it's not [], so it already exists
        else:
            result = results[0]

            new_text = request.values.get("quote", "")

            if new_text != "" and new_text is not None:
                result["quote"] = new_text
                # Save the edited command
                Quotes(
                    **result
                ).save()
            # No need for an else, if it's blank, then we'll just return
            #   the same exact quote object, no changes made

            to_return = [generate_packet(
                "quote",
                result["id"],
                {
                    "quote": str(result["quote"]),
                    "enabled": result["enabled"],
                    "channelId": result["channelId"],
                    "createdAt": str(result["createdAt"]),
                    "messageId": str(result["messageId"]),
                    "userId": result["userId"],
                    "userName": user["userName"]    # For packet generation
                },
                request.path,
                META_EDITED)
                         for result in results]

    return jsonify(to_return)


@APP.route("/api/v1/user/<string:username>", methods=["GET", "PATCH"])
def beam_user(username):
    # TODO: Auth checking

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
            - userName: <username> from request path
    """

    to_return = []
    meta = None

    results = retrieve_user(username)

    if request.method == "PATCH":
        # User doesn't exist, let's create it
        if results == []:
            result = User(
                active=True,
                confirmed_at=rethink.now(),
                email=request.values.get("email", ""),
                provider_id="{}${}".format(request.values.get("provider", ""),
                                           request.values.get("pid", "")),
                roles=[
                    "user"
                ],
                userName=username
            )

            meta = META_EDITED

            result.save()
        else:
            # User exists, so set the meta correctly
            meta = META_CREATED
    else:
        results = retrieve_user(username)

        to_return = [generate_packet("user",
                                     result["id"],
                                     {
                                         "userName": str(result["userName"]),
                                         "enabled": result["active"],
                                         "botUsername": str(result.get(
                                             "botUsername", None))
                                     },
                                     request.path,
                                     meta)
                     for result in results]

        return jsonify(to_return)


@APP.route("/api/v1/user/<string:username>/command", methods=["GET"])
def user_commands(username):

    """
    If you GET this endpoint, simply go to /api/v1/user/<username>/command with
    <username> replaced for the user you want to get commands for
    """
    users = retrieve_user(username)

    if len(users) < 1:
        return "", 204
    else:
        user = users[0]

    results = list(
        rethink.table("commands").filter(
            {
                "userId": user["id"],
                "deleted": False
            }
        ).run(g.rdb_conn))

    to_return = [generate_packet(
        "command",
        result["id"],
        {
            "name": str(result["name"]),
            "response": str(result["response"]),
            "enabled": result["enabled"],
            "channelId": result["channelId"],
            "createdAt": str(result["createdAt"]),
            "syntax": str(result["syntax"]),
            "help": str(result["help"]),
            "builtIn": result["builtIn"],
            "userName": user["userName"]
        },
        request.path) for result in results]

    return jsonify(to_return)


@APP.route("/api/v1/user/<string:username>/command/<string:cmd>",
           methods=["GET", "PATCH"])
def user_command(username, cmd):
    # TODO: Auth checking

    """
    If you GET this endpoint, go to /api/v1/user/<username>/command/<cmd> with
    <username> replaced for the user you want & <cmd> replaced with the command
    you wish to look up

    If you PATCH this endpoint:
        Go to /api/v1/user/<username>/command/<cmd> with <username> replaced
            for the user wanted & <cmd> replaced for the command you want to
            look up
        Parameters needed:
            - response: The new response for the command
    """

    # Get the first user object that matches the username
    users = retrieve_user(username)

    if len(users) < 1:
        return "", 204
    else:
        user = users[0]

    if request.method == "GET":
        results = list(rethink.table("commands").filter(
            {"userId": user["id"],
             "name": str(cmd)}
        ).run(g.rdb_conn))

        to_return = [generate_packet(
            "command",
            result["id"],
            {
                "name": str(result["name"]),
                "response": str(result["response"]),
                "enabled": result["enabled"],
                "channelId": result["channelId"],
                "createdAt": str(result["createdAt"]),
                "syntax": str(result["syntax"]),
                "help": str(result["help"]),
                "builtIn": result["builtIn"],
                "userName": user["userName"]
            },
            request.path)
                     for result in results]

        if len(to_return) > 0:
            to_return = to_return[0]

    elif request.method == "PATCH":

        results = list(rethink.table("commands").filter(
            {"userId": user["id"],
             "name": str(cmd)}
        ).run(g.rdb_conn))

        # It's [] (empty), so we need to make a NEW command
        if results == []:
            result = Commands(name=str(cmd),
                              response=request.values.get("response", ""),
                              channelId="2Cubed",
                              userLevel=0,
                              createdAt=rethink.now(),
                              userId=user["id"],
                              syntax="foo bar123",
                              help="lolnope",
                              enabled=True,
                              deleted=False,
                              builtIn=False)

            result.save()

            to_return = generate_packet(
                "command",
                result["id"],
                {
                    "name": str(result["name"]),
                    "response": str(result["response"]),
                    "enabled": result["enabled"],
                    "channelId": result["channelId"],
                    "createdAt": str(result["createdAt"]),
                    "syntax": str(result["syntax"]),
                    "help": str(result["help"]),
                    "builtIn": result["builtIn"],
                    "user": user["userName"]
                },
                request.path,
                META_CREATED)

        # it's not [], so it already exists
        else:
            result = results[0]

            new_response = request.values.get("response", "")

            if new_response != "" and new_response is not None:
                result["response"] = new_response

                # Save the edited command
                Commands(
                    **result
                ).save()

            to_return = [generate_packet(
                "command",
                result["id"],
                {
                    "name": str(result["name"]),
                    "response": str(result["response"]),
                    "enabled": result["enabled"],
                    "channelId": result["channelId"],
                    "createdAt": str(result["createdAt"]),
                    "syntax": str(result["syntax"]),
                    "help": str(result["help"]),
                    "builtIn": result["builtIn"],
                    "userName": user["userName"]
                },
                request.path,
                META_EDITED)
                         for result in results]

    return jsonify(to_return)
