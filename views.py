from flask import jsonify, request, g
from datetime import datetime
from run import app
from models import *
import rethinkdb as rethink
import remodel.connection

remodel.connection.pool.configure(db=app.config["RDB_DB"])


def retrieve_user(username):
    user = rethink.table("users").filter(
        lambda user:
            user["userName"].match("(?i){}".format(str(username)))
    ).limit(1).run(g.rdb_conn)

    return list(user)


def generate_packet(type, id, attributes, path, user, meta=None):
    """Parameters:
        type:   String of the data type being returned (user, command, etc.)
        id:     ID of whatever is being returned
        attributes: Dict of data attributes to return
        path:   String of endpoint being accessed for link generation
        user:   String of user provided to endpoint
        meta:   Dict of meta information, not required
    """

    print("type:\t", type)
    print("id:\t", id)
    print("attr:\t", attributes)
    print("path:\t", path)
    print("user:\t", user)

    if str(type).lower() == "user":
        relationships = {
            "commands": {
                "links": {
                    "self": "/api/v1/user/{}/relationships/commands".format(
                        str(user)),
                    "related": "/api/v1/user/{}/commands".format(str(user))
                }
            },
            "quotes": {
                "links": {
                    "self": "/api/v1/user/{}/relationships/quotes".format(
                        str(user)),
                    "related": "/api/v1/user/{}/quotes".format(str(user))
                }
            }
        }

    elif str(type).lower() == "command":
        relationships = {
            "user": {
                "links": {
                    "self": "/api/v1/user/{}/relationships".format(str(user)),
                    "related": "/api/v1/user/{}".format(str(user))
                }
            },
            "quotes": {
                "links": {
                    "self": "/api/v1/user/{}/relationships/quotes".format(
                        str(user)),
                    "related": "/api/v1/user/{}/quotes".format(str(user))
                }
            }
        }

    elif str(type).lower() == "quote":
        relationships = {
            "user": {
                "links": {
                    "self": "/api/v1/user/{}/relationships".format(str(user)),
                    "related": "/api/v1/user/{}".format(str(user))
                }
            },
            "commands": {
                "links": {
                    "self": "/api/v1/user/{}/relationships/commands".format(
                        str(user)),
                    "related": "/api/v1/user/{}/commands".format(str(user))
                }
            }
        }

    to_return = {
        "data": {
            "type": str(type),
            "id": str(id),
            "attributes": attributes,
            "relationships": relationships,
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


@app.before_request
def before_request():
    """Set the Flask session object's user to Flask-Login's current_user"""
    g.rdb_conn = rethink.connect(host=app.config["RDB_HOST"],
                                 port=app.config["RDB_PORT"],
                                 db=app.config["RDB_DB"])


@app.route("/api/v1/user/<username>", methods=["GET", "PATCH"])
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
            - userName: <username> from request path
    """

    to_return = []

    results = retrieve_user(username)

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

        meta = {
            "created": True,
            "updated": False
        }

        result.save()
    else:
        # User exists, so set the meta correctly
        meta = {
            "created": False,
            "updated": True
        }

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
                                 result["userName"],
                                 meta=meta) for result in results]

    return jsonify(to_return)


@app.route("/api/v1/user/<username>/command", methods=["GET"])
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

    results = list(rethink.table("commands").filter(
        {"userId": user["id"]}).run(g.rdb_conn))

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
                       "builtIn": result["builtIn"]
                   },
                   request.path,
                   user["userName"])
                 for result in results][0]

    return jsonify(to_return)


@app.route("/api/v1/user/<username>/command/<cmd>", methods=["GET", "PATCH"])
def user_command(username, cmd):

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
                            "builtIn": result["builtIn"]
                        },
                        request.path,
                        user["userName"])
                     for result in results]

    elif request.method == "PATCH":

        results = list(rethink.table("commands").filter(
            {"userId": user["id"],
             "name": str(cmd)}
        ).run(g.rdb_conn))

        print(results)

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
                                "builtIn": result["builtIn"]
                            },
                            request.path,
                            user["userName"],
                            meta={
                                "created": True,
                                "updated": False
                            })

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
                                "builtIn": result["builtIn"]
                            },
                            request.path,
                            user["userName"],
                            meta={
                                "created": False,
                                "updated": True
                            })
                         for result in results]

    return jsonify(to_return)
