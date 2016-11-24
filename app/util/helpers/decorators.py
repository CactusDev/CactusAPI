from functools import wraps
from flask import request


def check_limit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        limit = request.args.get("limit", None)
        if limit is not None and limit.isdigit():
            kwargs["limit"] = int(limit)
        return func(*args, **kwargs)
    return wrapper
