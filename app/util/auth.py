import json
from uuid import uuid4
from encodings.base64_codec import base64_encode
from functools import wraps
from flask import g, request


def scopes_required(scopes: set):
    def wrapper(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            data = request.get_json()
            print("json:\t", data)
            # if scopes.issubset(g.redis.exists())
            return f(*args, **kwargs)

        return decorated

    return wrapper


def generate_token():
    """
    Returns a Base64 encoded URL-safe auth token
    """

    # Return only the hash, minus the `==\n` from the end
    return base64_encode(uuid4().bytes)[0].decode()[:-3]


def validate_token(token, username):
    """
    Returns True if the user's token is valid, False if not
    """
    if "token" not in session:
        # There is not token object in the session, so user hasn't authed yet
        return False
    else:
        if session["token"]["username"] == username \
                and session["token"]["key"] == token:
            return True
        else:
            # Either the username or token did not match
            return False
