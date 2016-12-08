import rethinkdb as rethink

from . import (get_one, create_record, update_record, get_random,
               humanize_datetime, get_all, get_multiple, parse,
               resource_exists, json_api_response, validate_data)


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


def create_resource(table_name, model, data, *args, **kwargs):

    errors = validate_data(model, data)
    if errors is not None:
        return {}, errors, 400

    parsed, data, code = resource_exists(table_name, model, data, *args)

    # There was an error during pre-parsing, return that
    if code is not None:
        return {}, data, code

    if data is not None:
        changed = data
        code = 409
    else:
        changed = create_record(table_name, parsed)
        code = 201

    response = json_api_response(changed, table_name)

    try:
        return response, {}, code
    except TypeError as e:
        return {}, {"errors": e.args}, 400


def create_or_update(table_name, model, data, *args, **kwargs):

    errors = validate_data(model, data)
    if errors is not None:
        return {}, errors, 400

    parsed, data, code = resource_exists(table_name, model, data, *args)

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

    response = json_api_response(changed, table_name)

    return response, {}, code


def update_resource(table_name, model, data, *args, **kwargs):
    errors = validate_data(model, data)
    if errors is not None:
        return {}, errors, 400

    parsed, data, code = resource_exists(table_name, model, data, *args)

    # There was an error during pre-parsing, return that
    if code is not None:
        return {}, data, code

    if data is not None:
        # Don't change the createdAt
        if parsed.get("createdAt", None) is not None:
            del parsed["createdAt"]

    try:
        changed = update_record(table_name, {**parsed, "id": data["id"]})
        code = 200
    except rethink.ReqlOpFailedError as e:
        return {}, {"errors": e.args}, 500

    response = json_api_response(changed, table_name)

    return response, {}, code
