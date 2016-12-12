from datetime import datetime
from dateutil import parser
from uuid import UUID

from .rethink import get_one, get_all, get_random, get_multiple
from .parse import parse


def multi_response(table_name, model, random=False, **kwargs):
    response = []
    errors = []
    code = 200

    if "limit" not in kwargs:
        results = get_all(table_name, **kwargs)
    else:
        if random:
            results = get_random(table_name, **kwargs)
        else:
            results = get_multiple(table_name, **kwargs)

    for result in results:
        parsed, err, code = parse(model, result)
        if err != {}:
            errors.append(err)
            # Don't waste memory on adding a response object
            continue
        try:
            response.append(json_api_response(parsed, table_name))
        except TypeError as e:
            errors.append(e.args)

    return response, errors, code


def single_response(table_name, model, **kwargs):

    data = get_one(table_name, **kwargs)

    if data == {}:
        return {}, {}, 404

    parsed, errors, code = parse(model, data)

    response = {}

    if parsed is not None:
        # Try-except because json_api_response throws errors if stuff is bad
        try:
            return json_api_response(parsed, table_name), errors, code
        except TypeError as e:
            return {}, {"errors": e.args, **errors}, 400

    return response, errors, code


def json_api_response(data, resource):
    if not isinstance(resource, str):
        raise TypeError("resource argument must be type {}".format(str))

    if not isinstance(data, (list, dict)):
        raise TypeError(
            "data argument must be either type {} or {}".format(dict, list))

    if isinstance(data, dict):
        return {
            "id": data.pop("id"),
            "attributes": data,
            "type": resource
        }
    elif isinstance(data, list):
        return [{"id": obj.pop("id"), "attributes": obj, "type": resource}
                for obj in data]


def validate_uuid4(uuid_string):
    """Takes a string and checks if it's a valid UUID v4"""
    try:
        val = UUID(uuid_string, version=4)
    except ValueError:
        # It's not a valid UUID
        return False

    return val.hex == uuid_string.replace('-', '')


def humanize_datetime(to_humanize, *args):
    """
    Takes a marshalled JSON dict and a list of args to check OR a single string
    and converts that data into human-readable datetimes
    """
    # It's just a single string
    if args == ():
        return parser.parse(to_humanize).strftime("%c")

    # It's not just a single string
    if not isinstance(to_humanize, dict):
        raise TypeError("First argument MUST be a dict")

    # It's a dict
    for key in args:
        if not isinstance(key, str):
            raise TypeError("args must be a list of strings")
        # If the key exists, then convert it from the RethinkDB format to the
        # more human-readable date & time representation
        humanize = to_humanize.get(key, None)
        if humanize is not None:
            to_humanize[key] = parser.parse(humanize).strftime("%c")

    return to_humanize
