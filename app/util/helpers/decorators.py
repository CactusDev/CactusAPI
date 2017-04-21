from functools import wraps
from flask import request


class APIError(Exception):

    def __init__(self, *message, code):
        super().__init__(message)
        self.message = message
        self.code = code


class InternalServerError(Exception):

    def __init__(self):
        super().__init__()
        self.message = "Internal Server Error"
        self.code = 500


def catch_api_error(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (APIError, InternalServerError) as e:
            return {"errors": e.message}, e.code
    return wrapper


def check_random(func):
    """Checks if the request is being made with the ?random argument"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if request.values.get("random", '').lower() in ("true", '1'):
            if "limit" not in request.values:
                # By default return only 1 random quote
                kwargs["limit"] = 1

            kwargs["random"] = True

        return func(*args, **kwargs)
    return wrapper


def check_limit(func):
    """
    Checks if limit is an argument past in the request and if so, set's
    the 'limit' kwarg to equal it
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        limit = request.values.get("limit", None)
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


def pluralize_arg(func):
    """
    Checks if the first argument is a string and if so, pluralizes it in a
    simple way by tacking 's' on the end
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not isinstance(args[0], str):
            raise TypeError("first argument must be type {} to use"
                            "pluralize_arg".format(str))
        if not args[0].endswith('s'):
            args = (args[0] + 's', *args[1:])

        return func(*args, **kwargs)

    return wrapper
