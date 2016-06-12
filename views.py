from flask import jsonify, request
from datetime import datetime
from run import db, app
from models import *
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_
from sqlalchemy.ext.declarative import declarative_base


def generate_packet(type, id, attributes, path, user, meta=None):
    """Parameters:
        type:   String of the data type being returned (user, command, etc.)
        id:     ID of whatever is being returned
        attributes: Dict of data attributes to return
        path:   String of endpoint being accessed for link generation
        user:   String of user provided to endpoint
        meta:   Dict of meta information, not required
    """

    if str(type).lower() == "user":
        relationships = {
            "commands": {
                "links": {
                    "self": "/api/v1/user/{}/relationships/commands".format(str(user)),
                    "related": "/api/v1/user/{}/commands".format(str(user))
                }
            },
            "quotes": {
                "links": {
                    "self": "/api/v1/user/{}/relationships/quotes".format(str(user)),
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
                    "self": "/api/v1/user/{}/relationships/quotes".format(str(user)),
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
                    "self": "/api/v1/user/{}/relationships/commands".format(str(user)),
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


@app.route("/api/v1/user/<user>", methods=["GET"])
def beam_user(user):

    to_return = []

    results = Users.query.filter(Users.userName.ilike(str(user))).all()

    to_return = [ generate_packet("user",
                                  result.id,
                                  {
                                      "userName": str(result.userName),
                                      "enabled": result.enabled,
                                      "botUsername": str(result.botUsername)
                                  },
                                  request.path,
                                  result.userName) for result in results]

    return jsonify(to_return)


@app.route("/api/v1/user/<user>/command", methods=["GET"])
def user_commands(user):
    user = Users.query.filter(Users.userName.ilike(str(user))).one()
    results = Commands.query.filter_by(userId=user.id).all()

    to_return = [ generate_packet(
                    "command",
                    result.id,
                    {
                        "name": str(result.name),
                        "response": str(result.response),
                        "enabled": result.enabled,
                        "channelId": result.channelId,
                        "createdAt": str(result.createdAt),
                        "syntax": str(result.syntax),
                        "help": str(result.help),
                        "builtIn": result.builtIn
                    },
                    request.path,
                    user.userName)
                 for result in results]

    return jsonify(to_return)


@app.route("/api/v1/user/<user>/command/<cmd>", methods=["GET", "PATCH"])
def user_command(user, cmd):
    user = Users.query.filter(Users.userName.ilike(str(user))).one()

    if request.method == "GET":
        results = Commands.query.filter(and_(Commands.userId == user.id, Commands.name == str(cmd))).all()

        to_return = [ generate_packet(
                        "command",
                        result.id,
                        {
                            "name": str(result.name),
                            "response": str(result.response),
                            "enabled": result.enabled,
                            "channelId": result.channelId,
                            "createdAt": str(result.createdAt),
                            "syntax": str(result.syntax),
                            "help": str(result.help),
                            "builtIn": result.builtIn
                        },
                        request.path,
                        user.userName)
                     for result in results]

    elif request.method == "PATCH":

        results = Commands.query.filter(and_(Commands.userId == user.id, Commands.name == str(cmd))).all()

        # It's [] (empty), so we need to make a NEW command
        if results == []:
            command = Commands(name=str(cmd), response=request.args.get("response", ""), channelId="2Cubed", userLevel=0, createdAt=datetime.utcnow(), userId=user.id, syntax="foo bar123", help="lolnope")

            db.session.add(command)
            db.session.commit()

            to_return = [ generate_packet(
                            "command",
                            result.id,
                            {
                                "name": str(result.name),
                                "response": str(result.response),
                                "enabled": result.enabled,
                                "channelId": result.channelId,
                                "createdAt": str(result.createdAt),
                                "syntax": str(result.syntax),
                                "help": str(result.help),
                                "builtIn": result.builtIn
                            },
                            request.path,
                            user.userName,
                            meta={
                                "created": True,
                                "updated": False
                            })
                         for result in results]

        # it's not [], so it already exists
        else:
            result = results[0]

            result.response = request.values.get("response", "")
            db.session.add(result)
            db.session.commit()

            to_return = [ generate_packet(
                            "command",
                            result.id,
                            {
                                "name": str(result.name),
                                "response": str(result.response),
                                "enabled": result.enabled,
                                "channelId": result.channelId,
                                "createdAt": str(result.createdAt),
                                "syntax": str(result.syntax),
                                "help": str(result.help),
                                "builtIn": result.builtIn
                            },
                            request.path,
                            user.userName,
                            meta={
                                "created": False,
                                "updated": True
                            })
                         for result in results]

    return jsonify(to_return)
