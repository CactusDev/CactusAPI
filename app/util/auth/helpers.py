from functools import wraps
from flask import request


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
