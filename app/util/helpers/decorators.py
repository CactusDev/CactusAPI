from functools import wraps
from flask import request


def check_limit(func):
    """
    Checks if limit is an argument past in the request and if so, set's
    the 'limit' kwarg to equal it
    """
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
