from flask import request

from flask_restplus import Resource

from jose import jwt

from .. import api
from ..models import User
from ..util import helpers, auth


class Login(Resource):

    # TODO: Refactor after feature-freeze
    def post(self, **kwargs):
        json_data = request.get_json()

        if json_data == {}:
            return {"errors": ["Missing required authentication JSON"]}, 400

        if not {"token", "password"}.issubset(json_data.keys()):
            return {"errors": ["Missing either 'token' or 'password' "
                               "required keys"]}, 400

        user = helpers.get_one("users", token=json_data["token"])
        if user == {}:
            return {}, 404
        hashed_password = user.get("password")

        if hashed_password is None:
            return {
                "errors": ["User account is not configured for API access"]
            }, 400

        if not auth.verify_password(hashed_password, json_data["password"]):
            return {"errors": ["Username or password incorrect"]}, 400

        scopes = json_data.get("scopes", [])

        # Check scopes that are being requested by the user to see if the user
        # is allowed access to those resources
        if scopes == []:
            return {"errors": ["At least one scope must be requested"]}, 400

        data = {"token": json_data["token"],
                "scopes": scopes,
                "expires": auth.create_expires(seconds=45)}

        jw_token = jwt.encode(data, hashed_password, algorithm="HS512")

        return {"token": jw_token, "success": True}
