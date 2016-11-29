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


def lower_kwargs(*to_lower):
    """
    Takes a list of variables and if they exist in the request kwargs and
    they are strings, converts them to lowercase
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            path_data = {}
            for key in to_lower:
                if isinstance(kwargs[key], str):
                    path_data[key] = kwargs[key].lower()
                else:
                    path_data[key] = kwargs[key]

            return func(*args, path_data=path_data, **kwargs)
        return wrapper
    return decorator
