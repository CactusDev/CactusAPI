from flask import request
from collections import Iterable, Mapping

from .rethink import get_one


def convert(data):
    """Blech Marshmallow/Flask-RESTPlus hacky fix because otherwise death"""
    if isinstance(data, str) or isinstance(data, int):
        return str(data)
    elif isinstance(data, Mapping):
        return dict(map(convert, data.items()))
    elif isinstance(data, Iterable):
        return type(data)(map(convert, data))
    else:
        print("other:\t", data)
        return data


def get_mixed_args(*args):
    request_args = request.values
    request_json = request.get_json()

    if request_json is None:
        data = request_args
    else:
        data = {**request_args, **request_json}

    data = {key: value for key, value in data.items() if key not in args}

    return data


def validate_data(model, data, partial=False):
    """
    Validates the provided data against the provided model
    Returns None if successful, a dict of errors if otherwise
    """
    errors = model.schema.validate(data, partial=partial)

    if errors != {}:
        return errors

    return None


def resource_exists(table_name, **kwargs):
    # Check if anything exists that exactly copies that
    exists = get_one(table_name, **kwargs)

    if exists == {}:
        return {}, 404

    return exists, 200


def parse(model, data, partial=False):
    """Validates and dumps data into dict form"""

    data, errors = model.schema.load(data, partial=partial)

    if errors != {}:
        return {}, errors, 400

    dumped, errors = model.schema.dump(data)

    if errors != {}:
        return {}, errors, 400

    return dumped, {}, 200
