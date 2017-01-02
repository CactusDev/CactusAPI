from functools import wraps
from flask import request, jsonify
from jose import jwt, JWTError
from datetime import datetime

from ..helpers import get_one, APIError, return_error
from ... import app


def scopes_required(required_scopes):
    def wrapper(f):
        @wraps(f)
        @return_error
        def decorated(*args, **kwargs):
            """
            The endpoint is decorated, meaning it requires *some* form of
            authentication token in the X-Token-Auth header, return Forbidden
            X-Auth-Key - JWT token
            X-Auth-Token - Account token
            """
            jw_token = request.headers.get("X-Auth-Key", None)
            acct_token = request.headers.get("X-Auth-Token", None)

            if jw_token is None:
                missing = "X-Auth-Key"
                if acct_token is None:
                    missing += " and X-Auth-Token"

                raise APIError(
                    "Authentication header is incorrect. Missing required {}"
                    " header(s)".format(missing), code=403)

            user = get_one("users", token=acct_token)
            password = user.get("password")

            if user == {} or password is None:
                raise APIError(
                    "User account is not configured for API access", code=403)

            exists = get_one("keys", token=acct_token)
            if exists == {}:
                raise APIError(
                    "Invalid authentication key",
                    "Token's user account not currently authenticated",
                    code=403)

            else:
                if exists.get("key", "") != jw_token:
                    raise APIError(
                        "Invalid authentication key",
                        "Supplied key does not match any currently valid keys",
                        code=403)

                time_now = datetime.timestamp(datetime.utcnow())
                if time_now > exists.get("expiration", 0):
                    return {
                        "errors": [
                            "Invalid authentication key",
                            "Key has expired"
                        ]
                    }, 403

            try:
                decoded = jwt.decode(jw_token, password, algorithms="HS512")
            except JWTError as e:
                raise APIError(*[arg.args for arg in e.args], code=403)

            if acct_token != decoded.get("token", ""):
                raise APIError("User token and JWT key do not match", code=403)

            token_scopes = set()
            API_SCOPES = app.config.get("API_SCOPES", {})

            if API_SCOPES == {}:
                print("WARNING! API_SCOPES IS NOT CONFIGURED")

            i = 0
            bits = decoded.get("scopes", "")

            for scope in bits:
                if scope == '1':
                    for k, v in API_SCOPES.items():
                        if v == i:
                            token_scopes.add(k)

                i += 1

            allowed = required_scopes.difference(token_scopes)

            # The scopes allowed for this JWT do not contain all of the
            # required scopes for this endpoint
            if allowed:
                raise APIError(
                    {
                        "message": "Scopes allowed for that access token "
                        "do not meet endpoint requirements",
                        "missing": list(allowed)
                    }, code=403)

            # Passed the scopes requirements, return the endpoint's response
            return f(*args, **kwargs)

        return decorated

    return wrapper
