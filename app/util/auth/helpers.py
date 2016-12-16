from functools import wraps
from flask import request
from jose import jwt, JWTError
from ..helpers import get_one


def scopes_required(scopes):
    def wrapper(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            data = request.headers.get('X-Token-Auth', []).split('-')
            # The endpoint is decorated, meaning it requires *some* form of
            # authentication token in the X-Token-Auth header, return Forbidden
            # Format: <JWT token>-<username token>

            if len(data) < 2:
                return {}, {"errors": ["X-Token-Auth header is incorrect "
                                       "format. Must be of format "
                                       " <JWT token>-<account token>"]
                            }, 403

            user = get_one("users", token=data[1])
            password = user.get("password")

            if user == {} or password is None:
                return {}, {
                    "errors": ["User account is not configured for API access"]
                }, 403

            try:
                jwt_token = jwt.decode(data, password, algorithims="RS512")
            except JWTError as e:
                return {}, {"errors": e.args}, 403

            if data[1] != jwt_token.get("token", ""):
                return {}, {
                    "errors": [
                        "Provided user token and JWT token do not match!"]
                }, 403

            allowed = set(jwt_token.get("scopes", [])).issuperset(scopes)

            # The scopes allowed for this JWT do not contain all of the
            # required scopes for this endpoint
            if not allowed:
                return {}, {
                    "errors": [
                        "Scopes allowed for that JWT token do not meet "
                        "endpoint requirements"]
                }, 403

            # Passed the scopes requirements, return the endpoint's response
            return f(*args, **kwargs)

        return decorated

    return wrapper
