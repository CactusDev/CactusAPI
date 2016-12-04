from uuid import UUID

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


def _pre_parse(table_name, model, data, filter_keys):
    # Validate the data from the route code and serialize it into dict form
    parsed, errors, code = parse(model, data)

    if errors != {}:
        return {}, errors, code

    if not isinstance(filter_keys, list):
        raise TypeError("filter_keys must be a list of strings")

    # Not needed currently, but may be later in development
    # filter_keys += [kwarg for kwarg in kwargs.keys()]

    for key in filter_keys:
        if not isinstance(key, str):
            raise TypeError("Each key in filter_keys must be a string")

    filter_data = {key: parsed[key] for key in filter_keys}

    # Check if anything exists that exactly copies that
    exists = get_one(table_name, **filter_data)

    return parsed, exists, None


def parse(model, data):

    errors = model.schema.validate(data)

    # HACK: Need to figure out how to fix _schema: ["Invalid type"] error to
    # actually be more useful
    if errors != {}:
        if "_schema" in errors.get("response", {}):
            del errors["response"]["_schema"]
            errors["response"]["response"] = "Missing data for required field"

    if errors != {}:
        # TODO: Make this return proper HTTP error codes
        return None, errors, 400

    dumped, errors = model.schema.dump(model(**data))

    return dumped, errors, 200


def random_response(table_name, model, limit=1, **kwargs):
    response = []
    errors = []
    code = 200

    results = get_random(table_name, limit=limit, **kwargs)

    for result in results:
        parsed, err, code = parse(model, result)
        parsed = humanize_datetime(parsed, ["createdAt"])
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


def multi_response(table_name, model, **kwargs):
    response = []
    errors = []
    code = 200

    if "limit" not in kwargs:
        results = get_all(table_name, **kwargs)
    else:
        results = get_multiple(table_name, **kwargs)

    for result in results:
        parsed, err, code = parse(model, result)
        parsed = humanize_datetime(parsed, ["createdAt"])
        response.append({
            "id": parsed.pop("id"),
            "attributes": parsed,
            "type": table_name
        })
        if err != {}:
            errors.append(err)

    return response, errors, code


def single_response(table_name, model, **kwargs):

    data = get_one(table_name, **kwargs)

    if data is None:
        return {}, {}, 404

    parsed, errors, code = parse(model, data)

    response = {}

    if parsed is not None:
        response = humanize_datetime(parsed, ["createdAt"])

        response = {
            "id": response.pop("id"),
            "attributes": response,
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

    changed = humanize_datetime(changed, ["createdAt"])

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

        changed = update_record(
            table_name, {**parsed, "id": data["id"]})

        code = 200
    else:
        changed = create_record(table_name, parsed)
        code = 201

    if isinstance(changed, Exception):
        return {"errors": changed.args}, 500

    changed = humanize_datetime(changed, ["createdAt"])

    response = {
        "id": changed.pop("id"),
        "attributes": changed,
        "type": table_name
    }

    return response, {}, code
