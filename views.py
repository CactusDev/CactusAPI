"""Views for the API"""

# TODO: Fix DELETE endpoints everywhere
# TODO: Implement proper error packet creation/return

import time
from datetime import datetime, timedelta
import remodel.connection
import requests
import pytz
import redis
import rethinkdb as rethink
from uuid import uuid4
from flask import jsonify, request, g, make_response
from models import User, Commands, Quotes, Messages, Friend

from run import APP

remodel.connection.pool.configure(db=APP.config["RDB_DB"])
REDIS_CONN = redis.Redis()

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


def generate_error(meta=None, **kwargs):
    """Create and return a JSON-API compliant error packet

    All parameters are optional

    Parameters:
        uid:            Unique ID for this individual error
        links:          An object containing an about key that is a link that
                            leads to further details about this particular
                            occurrence of the problem.
        status:         the HTTP status code applicable to this problem,
                            expressed as a string value.
        code:           an application-specific error code, a string value.
        title:          Short, human-readable summary of the problem.
                            SHOULD NOT CHANGE between occurences of problem
        detail:         Human-readable explanation specific to this problem
        source:         An object containing references to the source of the
                            error
        meta:           Dict of meta information, NOT required
    """

    packet = {}
    errors = {}

    correct_types = {
        "uid": None,
        "links": dict,
        "status": str,
        "code": str,
        "title": str,
        "detail": str,
        "source": dict,
        "meta": dict
    }

    # Remove any non-standard arguments
    packet = {key: kwargs[key] for key in kwargs if key in correct_types}

    print(type(packet["source"]))
    print(isinstance(packet["source"], correct_types["source"]))

    # Check all of the included arguments are of the proper type
    for arg in packet:
        if correct_types[arg] is not None and \
                not isinstance(packet[arg], correct_types[arg]):
            errors[arg] = "incorrect type {}, should be type {}".format(
                arg.__class__.__name__, correct_types[arg].__name__
                )

    if "links" in packet:
        if "about" in packet["links"]:
            if not isinstance(packet["links"]["about"], str):
                errors["links:about"] = "link 'about' key is not a string"
        else:
            errors["links"] = "link key does not contain required 'about' key"

    if "source" in packet and not isinstance(packet["source"], dict):
        errors["source"] = "'source' key is not a dict"

    if meta is not None and isinstance(meta, dict):
        to_return["meta"] = meta

    return (packet, None) if len(errors) == 0 else (None, errors)


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


@APP.route("/api/v1/channel/<int:channel>/friend", methods=["GET"])
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
        },
        request.path
    ) for result in results]

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
        friend you want to edit or create.
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

        result = friend_query.limit(1).run(g.rdb_conn).items[0]

        to_return = generate_packet(
            "friend",
            result["id"],
            {
                "channelId": result["channelId"],
                "userName": result["userName"],
                "userId": result["userId"],
                "active": result["active"]
            },
            request.path
        )

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
            # Newly created, so it needs to be 201
            code = 201

        else:
            # Get the first result, only want to edit one
            result = results[0]
            # Get length seperately so it's easier to reference
            # + .0 is required to convert it to a float
            length = request.values.get("length", 0) + .0

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
            # Success - 200
            code = 200

        is_active = result["expires"] != rethink.epoch_time(0) and \
            result["expires"] > rethink.epoch_time(time.time())

        active = True if is_active else False

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
                "expiresAt": expires
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

                # We deleted something so nothing has to be returned
                to_return = {"deleted": results[0]["id"], "success": True}
                code = 200

            except Exception as error:
                print("Exception caught! views:225")
                print(error)

                # Ruh roh, errors happened.
                to_return = {
                    "deleted": None,
                    "success": False,
                    "error": error
                }
                code = 500

        # If we're here there's no need to else
        # This far means that there were NO results
        to_return = {
            "deleted": None,
            "success": False,
            "error": "Friend {} does not exist".format()}
        code = 404

    return make_response(jsonify(to_return), code)


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
        },
        request.path
    ) for result in results]

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


@APP.route("/api/v1/channel/<string:channel>/quote", methods=["GET"])
def user_quotes(channel):
    """
    If you GET this endpoint, go to /api/v1/channel/<channel>/quote
    with <channel> replaced for the channel you want to get quotes for
    """

    # Get all users that match the channel
    users = retrieve_user(channel)

    # Were any returned?
    if len(users) < 1:
        # No, return 204 since it's not an error, the user just doesn't exist
        return jsonify(None), 204
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


@APP.route("/api/v1/channel/<string:channel>/quote/<string:quote>",
           methods=["GET", "PATCH", "DELETE"])
def chan_quote(channel, quote):
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
            - quote: The new contents of the quote

    If you DELETE this endpoint:
        Go to /api/v1/channel/<channel>/quote/<quote> with <channel> replaced
        for the channel you want and <quote> replaced with the quote ID you
        want to remove
    """

    # Get all users that match the channel
    users = retrieve_user(channel)

    # Were any returned?
    if len(users) < 1:
        # No, return 204 since it's not an error, the user just doesn't exist
        return jsonify(None), 204
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
            rethink.table("quotes").filter(
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
                # Save the edited quote
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

    elif request.method == "DELETE":

        results = list(rethink.table("quotes").limit(1).run(g.rdb_conn))

        # If the user DOES exist in the DB in the quote table
        if results != []:
            try:
                rethink.table("quotes").get(
                    results[0]["id"]).delete().run(g.rdb_conn)

                return make_response(jsonify(None), 204)

            except Exception as error:
                print("Exception caught! views:225")
                print(error)

                return make_response(jsonify([{"error": error}]), 500)

    return jsonify(to_return)


@APP.route("/api/v1/user/<string:username>",
           methods=["GET", "PATCH", "DELETE"])
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
    """

    to_return = []
    meta = None

    results = retrieve_user(username)

    if request.method == "GET":
        if results == []:
            # Nothing exists for that user
            to_return, errors = generate_error(
                uid=str(uuid4()),
                status="404",
                title="Requested 'user' Resource Does Not Exist",
                detail="The requested user '{}' does not exist".format(
                    username),
                source={"pointer": request.path}
            )

            if errors is not None:
                print("ERRARS!")
                print(errors)

            code = 404
        else:
            code = 200

    elif request.method == "PATCH":
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

            meta = META_CREATED
            code = 200

            result.save()
        else:
            # Take the first one
            result = results[0]

            for key in request.values:
                if key in result and request.values.get(key) != "" and \
                        request.values.get(key) is not None:
                    result[key] = request.values.get(key)

            # Set the values of that object and save changes
            User(
                **result
            ).save()

            # User exists, and we edited it, so set the meta correctly
            meta = META_EDITED
            code = 200

        results = retrieve_user(username)

    elif request.method == "DELETE":
        results = retrieve_user(username)

        # If the user DOES exist in the DB in the users table
        if results != []:
            try:
                rethink.table("users").get(
                    results[0]["id"]).delete().run(g.rdb_conn)

                return make_response(jsonify(None), 204)

            except Exception as error:
                print("Exception caught! views:774")
                print(error)

                return make_response(jsonify([{"error": error}]), 500)

    # If to_return still has it's initialization value of None, then there
    # were no errors, and go ahead with creating the success packet
    if to_return == []:
        to_return = [generate_packet("user",
                                     result["id"],
                                     {
                                         "userName": result["userName"],
                                         "enabled": result["active"],
                                         "botUsername": str(result.get(
                                             "botUsername", None))
                                     },
                                     request.path,
                                     meta)
                     for result in results]
    else:
        to_return = {
            "jsonapi": {
                "version": "1.0"
            },
            "errors": [to_return]
        }

    print(to_return)

    return make_response(jsonify(to_return), code)


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
           methods=["GET", "PATCH", "DELETE"])
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
            - level:    An integer for the user level required to run the
                        command.
                            0 - Accessible by ALL users
                            1 - Channel Moderator Only
                            2 - Channel Owner Only
                            3 - Channel Subscriber Only
    """

    # Get the first user object that matches the username
    users = retrieve_user(username)

    if len(users) < 1:
        return "", 204
    else:
        user = users[0]

    if request.method == "GET":
        result = list(rethink.table("commands").filter(
            {"userId": user["id"],
             "name": cmd}
        ).limit(1).run(g.rdb_conn))[0]

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
                "userName": user["userName"],
                "level": result["level"]
            },
            request.path)

        if len(to_return) > 0:
            to_return = to_return

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
                              builtIn=False,
                              level=request.values.get("level", 0))

            result.save()

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
                    "user": user["userName"],
                    "level": result["level"]
                },
                request.path,
                META_CREATED)]

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

    elif request.method == "DELETE":

        results = list(rethink.table("commands").limit(1).run(g.rdb_conn))

        # If the user DOES exist in the DB in the friend table
        if results != []:
            try:
                rethink.table("commands").get(
                    results[0]["id"]).delete().run(g.rdb_conn)

                return make_response(jsonify(None), 204)

            except Exception as error:
                print("Exception caught! views:225")
                print(error)

                return make_response(jsonify([{"error": error}]), 500)

    return jsonify(to_return)
