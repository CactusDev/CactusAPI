from flask import request
from flask_restplus import Resource
from jose import jwt
import redis

from .. import api, app
from ..models import User
from ..util import helpers, auth


class Login(Resource):

    # Will be implemented later if need be for token revocation, but not used
    @helpers.lower_kwargs("token")
    def delete(self, path_data, **kwargs):
        pass

    # TODO: Refactor after feature-freeze
    def post(self, **kwargs):
        data = helpers.get_mixed_args()

        if data == {}:
            return {"errors": ["Missing required authentication JSON"]}, 400

        if not {"token", "password"}.issubset(data.keys()):
            return {"errors": ["Missing either 'token' or 'password' "
                               "required keys"]}, 400

        user = helpers.get_one("users", token=data["token"])
        if user == {}:
            return {"errors": ["User account does not exist"]}, 404
        hashed_password = user.get("password")

        if hashed_password is None:
            return {
                "errors": ["User account is not configured for API access"]
            }, 400

        if not auth.verify_password(hashed_password, data["password"]):
            return {"errors": ["Username or password incorrect"]}, 400

        scopes = data.get("scopes", [])

        # TODO: Update API documentation explaining to request multiple scopes
        # split with spaces

        # TODO: Validate requested scopes against set of defined scopes
        # in config (API_SCOPES)
        # HACK: For now, just hard-code it. Fix after feature-freeze
        API_SCOPES = {
            "alias:create", "alias:manage",
            "command:create", "command:manage",
            "config:create", "config:manage",
            "quote:create", "quote:manage",
            "repeat:create", "repeat:manage",
            "social:create", "social:manage",
            "trust:create", "trust:manage",
        }

        if isinstance(scopes, str):
            scopes = scopes.split()

        # Parse out non-valid scopes
        scopes = [scope for scope in scopes if scope in API_SCOPES]

        # Check scopes that are being requested by the user to see if the user
        # is allowed access to those resources
        if scopes == []:
            return {"errors": ["At least one scope must be requested"]}, 400

        to_encode = {"token": data["token"], "scopes": scopes}

        jw_token = jwt.encode(to_encode, hashed_password, algorithm="HS512")

        # TODO: Find out if this is a security problem including the scopes
        return {"token": jw_token, "scopes": scopes}
