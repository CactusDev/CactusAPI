from uuid import UUID
from dateutil import parser
import rethinkdb as rethink

from . import (get_one, create_record, update_record, get_random,
               humanize_datetime, get_all, get_multiple)


def validate_uuid4(uuid_string):
    """Takes a string and checks if it's a valid UUID v4"""
    try:
        val = UUID(uuid_string, version=4)
    except ValueError:
        # It's not a valid UUID
        return False

    return val.hex == uuid_string.replace('-', '')


def _pre_parse(table_name, model, data, partial=False, *args):
    # Validate the data from the route code and serialize it into dict form
    parsed, errors, code = parse(model, data, partial=partial)

    if errors != {}:
        return {}, errors, code

    # Not needed currently, but may be later in development
    # filter_keys += [kwarg for kwarg in kwargs.keys()]

    for key in args:
        if not isinstance(key, str):
            raise TypeError("Each filter key must be type {}".format(str))

    filter_data = {key: parsed[key] for key in args}

    # Check if anything exists that exactly copies that
    exists = get_one(table_name, **filter_data)

    return parsed, exists, None


def parse(model, data, partial=False):

    errors = model.schema.validate(data, partial=partial)

    # HACK: Need to figure out how to fix _schema: ["Invalid type"] error to
    # actually be more useful
    if errors != {}:
        if "_schema" in errors.get("response", {}):
            del errors["response"]["_schema"]
            errors["response"]["response"] = "Missing data for required field"

    if errors != {}:
        # TODO: Make this return proper HTTP error codes
        return None, errors, 400

    print(data)

    data, errors = model.schema.load(data, partial=partial)

    if errors != {}:
        return {}, errors, 400

    dumped, errors = model.schema.dump(data)

    print(dumped)

    return dumped, errors, 200


def multi_response(table_name, model, random=False, **kwargs):
    response = []
    errors = []
    code = 200

    if "limit" not in kwargs:
        results = get_all(table_name, **kwargs)
    else:
        if random:
            results = get_random(table_name, limit=kwargs["limit"], **kwargs)
        else:
            results = get_multiple(table_name, **kwargs)

    for result in results:
        parsed, err, code = parse(model, result)
        if err != {}:
            errors.append(err)
            # Don't waste memory on adding a response object
            continue
        response.append({
            "id": parsed.pop("id"),
            "attributes": parsed,
            "type": table_name
        })

    return response, errors, code


def single_response(table_name, model, **kwargs):

    data = get_one(table_name, **kwargs)

    if data is None:
        return {}, {}, 404

    parsed, errors, code = parse(model, data)

    response = {}

    if parsed is not None:
        response = {
            "id": parsed.pop("id"),
            "attributes": parsed,
            "type": table_name
        }

    return response, errors, code


def create_or_none(table_name, model, data, filter_keys, **kwargs):
    # TODO Move filter_keys list to *args

    parsed, data, code = _pre_parse(table_name, model, data, filter_keys)

    # There was an error during pre-parsing, return that
    if code is not None:
        return {}, data, code

    if data is not None:
        changed = data
        code = 409
    else:
        changed = create_record(table_name, parsed)
        code = 201

    response = {
        "id": changed.pop("id"),
        "attributes": changed,
        "type": table_name
    }

    return response, {}, code


def create_or_update(table_name, model, data, filter_keys, **kwargs):
    parsed, data, code = _pre_parse(table_name, model, data, filter_keys)

    # There was an error during pre-parsing, return that
    if code is not None:
        return {}, data, code

    if data is not None:
        # Don't change the createdAt
        if parsed.get("createdAt", None) is not None:
            del parsed["createdAt"]

        changed = update_record(table_name, {**parsed, "id": data["id"]})
        code = 200

    else:
        changed = create_record(table_name, parsed)
        code = 201

    if isinstance(changed, Exception):
        return {}, {"errors": changed.args}, 500

    response = {
        "id": changed.pop("id"),
        "attributes": changed,
        "type": table_name
    }

    return response, {}, code


def update_resource(table_name, model, data, *args, **kwargs):
    parsed, data, code = _pre_parse(table_name, model, data, partial=True,
                                    *args)

    # There was an error during pre-parsing, return that
    if code is not None:
        return {}, data, code

    # Don't change the createdAt
    if parsed.get("createdAt", None) is not None:
        del parsed["createdAt"]

    try:
        changed = update_record(table_name, {**parsed, "id": data["id"]})
        code = 200
    except rethink.ReqlOpFailedError as e:
        return {}, {"errors": e.args}, 500

    response = {
        "id": changed.pop("id"),
        "attributes": changed,
        "type": table_name
    }

    return response, {}, code
