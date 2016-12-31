from functools import wraps
from flask import request, jsonify
from jose import jwt, JWTError
from datetime import datetime

from ..helpers import get_one


def scopes_required(required_scopes):
    def wrapper(f):
        @wraps(f)
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

                return {"errors": ["Authentication header is incorrect. "
                                   "Missing required {} "
                                   "header(s)".format(missing)]
                        }, 403

            exists = get_one("keys", token=acct_token)

            if exists == {}:
                return {
                    "errors": [
                        "Invalid authentication key",
                        "No users currently authenticated for that token"
                    ]
                }, 403
            else:
                if exists.get("key", "") != jw_token:
                    return {
                        "errors": [
                            "Invalid authentication key",
                            "Supplied key does not match any currently valid"
                            " keys"
                        ]
                    }, 403

                time_now = datetime.timestamp(datetime.utcnow())
                if time_now > exists.get("expiration", 0):
                    return {
                        "errors": [
                            "Invalid authentication key",
                            "Key has expired"
                        ]
                    }, 403

            user = get_one("users", token=acct_token)
            password = user.get("password")

            if user == {} or password is None:
                return {
                    "errors": ["User account is not configured for API access"]
                }, 403

            try:
                decoded = jwt.decode(jw_token, password, algorithms="HS512")
            except JWTError as e:
                return {"errors": [arg.args for arg in e.args]}, 403

            if acct_token != decoded.get("token", ""):
                return {
                    "errors": [
                        "Provided user token and JWT token do not match!"]
                }, 403

            token_scopes = set(decoded.get("scopes", []))

            allowed = required_scopes.difference(token_scopes)

            # The scopes allowed for this JWT do not contain all of the
            # required scopes for this endpoint
            if len(allowed):
                return {
                    "errors": [
                        {
                            "message": "Scopes allowed for that access token "
                            "do not meet endpoint requirements",
                            "missing": list(allowed)
                        }
                    ]
                }, 403

            # Passed the scopes requirements, return the endpoint's response
            return f(*args, **kwargs)

        return decorated

    return wrapper
