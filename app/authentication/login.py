from flask import request
from flask_restplus import Resource
from jose import jwt

from .. import api, app
from ..models import User
from ..util import helpers, auth
from ..util.helpers import APIError


class Login(Resource):

    # Will be implemented later if need be for token revocation, but not used
    @helpers.lower_kwargs("token")
    def delete(self, path_data, **kwargs):
        pass

    # TODO: Refactor after feature-freeze
    @helpers.return_error
    def post(self, **kwargs):
        data = helpers.get_mixed_args()

        if data == {}:
            raise APIError("Missing required authentication JSON", code=400)

        if not {"token", "password"}.issubset(data.keys()):
            raise APIError(
                "Missing either 'token' or 'password' required keys", code=400)

        # TODO: limit authentication requests to 5/minute
        user = helpers.get_one("users", token=data["token"])
        if user == {}:
            raise APIError("User account does not exist", code=404)

        hashed_password = user.get("password")

        if hashed_password is None:
            raise APIError("User account is not configured for API access",
                           code=403)

        if not auth.verify_password(hashed_password, data["password"]):
            raise APIError("Username or password incorrect", code=400)

        scopes = data.get("scopes", [])

        # TODO: Update API documentation explaining to request multiple scopes
        # split with spaces
        API_SCOPES = app.config.get("API_SCOPES", {})

        if API_SCOPES == {}:
            print("WARNING!  API_SCOPES IS NOT CONFIGURED")

        if isinstance(scopes, str):
            scopes = scopes.split()

        bits = list("00000000000000")

        scopes = [scope for scope in scopes if scope in API_SCOPES.keys()]

        # Parse out non-valid scopes and convert to bit string
        for scope in scopes:
            if scope in API_SCOPES:
                bits[API_SCOPES[scope]] = "1"

        bits = ''.join(bits)

        # Check scopes that are being requested by the user to see if the user
        # is allowed access to those resources
        if scopes == []:
            return {"errors": ["At least one scope must be requested"]}, 400

        to_encode = {"token": data["token"], "scopes": bits}

        jw_token = jwt.encode(to_encode, hashed_password, algorithm="HS512")

        exists = helpers.get_one("keys", token=data["token"])

        key_store = {
            **to_encode,
            "expiration": auth.create_expires(
                **app.config.get("AUTH_EXPIRATION", {"days": 1})),
            "key": jw_token
        }

        if exists == {}:
            helpers.create_record("keys", key_store)
        else:
            helpers.update_record("keys", {**exists, **key_store})

        # TODO: Find out if this is a security problem including the scopes
        return {"token": jw_token, "scopes": scopes}
