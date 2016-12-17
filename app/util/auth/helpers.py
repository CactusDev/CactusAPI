from functools import wraps
from flask import request
from jose import jwt, JWTError
from ..helpers import get_one


def scopes_required(scopes):
    def wrapper(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            # The endpoint is decorated, meaning it requires *some* form of
            # authentication token in the X-Token-Auth header, return Forbidden
            # X-Auth-JWT - JWT token
            # X-Auth-Token - Account token

            jw_token = request.headers.get("X-Auth-JWT", None)
            acct_token = request.headers.get("X-Auth-Token", None)

            if jw_token is None:
                missing = "X-Auth-JWT"
                if acct_token is None:
                    missing += " and X-Auth-Token"

                return {}, {"errors": ["X-Token-Auth header is incorrect. "
                                       "Missing required {} "
                                       "header(s)".format(missing)]
                            }, 403

            user = get_one("users", token=acct_token)
            password = user.get("password")

            if user == {} or password is None:
                return {}, {
                    "errors": ["User account is not configured for API access"]
                }, 403

            try:
                decoded = jwt.decode(jw_token, password, algorithms="HS512")
                print(decoded)
            except JWTError as e:
                return {}, {"errors": e.args}, 403

            if acct_token != decoded.get("token", ""):
                return {}, {
                    "errors": [
                        "Provided user token and JWT token do not match!"]
                }, 403

            allowed = set(decoded.get("scopes", [])).issuperset(scopes)

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
