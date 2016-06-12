from flask import jsonify, request
from datetime import datetime
from run import db, app
from models import *
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_
from sqlalchemy.ext.declarative import declarative_base


@app.route("/api/v1/user/<user>", methods=["GET"])
def beam_user(user):

    to_return = []

    results = Users.query.filter(Users.userName.ilike(str(user))).all()

    to_return = [{
        "data": [
            {
                "type": "user",
                "id": str(result.id),
                "attributes": {
                    "userName": str(result.userName),
                    "enabled": result.enabled,
                    "botUsername": str(result.botUsername)
                }
            }]
    } for result in results]

    return jsonify(to_return)


@app.route("/api/v1/user/<user>/commands", methods=["GET"])
def user_commands(user):
    user = Users.query.filter(Users.userName.ilike(str(user))).one()
    results = Commands.query.filter_by(userId=user.id).all()

    to_return = [{
        "data": [
            {
                "type": "commands",
                "id": str(result.id),
                "attributes": {
                    "name": str(result.name),
                    "response": str(result.response),
                    "enabled": result.enabled,
                    "channelId": result.channelId,
                    "createdAt": str(result.createdAt),
                    "syntax": str(result.syntax),
                    "help": str(result.help),
                    "builtIn": result.builtIn
                }
            }]
    } for result in results]

    return jsonify(to_return)


@app.route("/api/v1/user/<user>/commands/<cmd>", methods=["GET", "PUT"])
def user_command(user, cmd):
    user = Users.query.filter(Users.userName.ilike(str(user))).one()

    if request.method == "GET":
        results = Commands.query.filter(and_(Commands.userId == user.id, Commands.name == str(cmd))).all()

        to_return = [{
            "data": [
                {
                    "type": "command",
                    "id": str(result.id),
                    "attributes": {
                        "name": str(result.name),
                        "response": str(result.response),
                        "enabled": result.enabled,
                        "channelId": result.channelId,
                        "createdAt": str(result.createdAt),
                        "syntax": str(result.syntax),
                        "help": str(result.help),
                        "builtIn": result.builtIn
                    }
                }]
        } for result in results]

    elif request.method == "PUT":

        print(user.userName)

        results = Commands.query.filter(and_(Commands.userId == user.id, Commands.name == str(cmd))).all()

        print(results)

        # It's [] (empty), so we need to make a NEW command
        if results == []:
            command = Commands(name=str(cmd), response=request.args.get("response", ""), channelId="2Cubed", userLevel=0, createdAt=datetime.utcnow(), userId=user.id, syntax="foo bar123", help="lolnope")

            db.session.add(command)
            db.session.commit()

            to_return = [{
                "data": [
                    {
                        "type": "command",
                        "id": str(command.id),
                        "attributes": {
                            "name": str(command.name),
                            "response": str(command.response),
                            "enabled": command.enabled,
                            "channelId": command.channelId,
                            "createdAt": str(command.createdAt),
                            "syntax": str(command.syntax),
                            "help": str(command.help),
                            "builtIn": command.builtIn
                        }
                    }
                ],
                "meta": {
                    "created": True,
                    "updated": False
                }
            }]
        # it's not [], so it already exists
        else:
            result = results[0]

            result.response = request.values.get("response", "")
            db.session.add(result)
            db.session.commit()

            to_return = [
                {
                    "data": [
                        {
                            "type": "command",
                            "id": str(result.id),
                            "attributes": {
                                "name": str(result.name),
                                "response": str(result.response),
                                "enabled": result.enabled,
                                "channelId": result.channelId,
                                "createdAt": str(result.createdAt),
                                "syntax": str(result.syntax),
                                "help": str(result.help),
                                "builtIn": result.builtIn
                            }
                        }
                    ],
                    "meta": {
                        "created": False,
                        "updated": True
                    }
                }]

    return jsonify(to_return)
