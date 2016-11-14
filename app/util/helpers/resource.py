from datetime import datetime
from flask import g, request

from flask_restplus import marshal
from marshmallow import Schema

from ... import models

from . import (get_one, create_record, update_record,
               humanize_datetime, exists, get_all, get_multiple)


def parse(model, data):

    dumped, errors = model.schema.dump(model(**data))

    code = 200 if errors == {} else 400

    return dumped, errors, code


def multi_response(table_name, model, filter_data, limit=None):
    response = []
    errors = []
    code = 200
    if limit is not None:
        results = get_all(table_name, **filter_data)
    else:
        results = get_multiple(table_name, limit=limit, **filter_data)

    for result in results:
        parsed, err, code = parse(model, result)
        response.append({
            "attributes": humanize_datetime(parsed, ["createdAt"]),
            "type": table_name,
            "id": result.pop("id")
        })
        errors.append(err if err != {} else None)

    if errors == {}:
        errors = None

    return response, errors, code


def single_response(table_name, model, filter_data):
    data = get_one(table_name, **filter_data)

    if data is None:
        return {}, {}, 404

    parsed, errors, code = parse(model, data)

    response = humanize_datetime(parsed, ["createdAt"])

    response = {
        "id": response.pop("id"),
        "attributes": response,
        "type": table_name
    }

    return response, errors, code


def create_or_update(table_name, model, data, filter_keys, **kwargs):
    # Validate the data from the route code and serialize it into dict form
    parsed, errors, code = parse(model, data)

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

    if exists is not None:
        # Don't change the createdAt
        if parsed.get("createdAt", None) is not None:
            del parsed["createdAt"]

        changed = update_record(
            table_name, {**parsed, "id": exists["id"]})
        code = 200
    else:
        changed = create_record(table_name, parsed)
        code = 201

    if isinstance(changed, Exception):
        return {"errors": changed.args}, 500

    changed = humanize_datetime(changed, ["createdAt"])

    response = {
        "attributes": changed,
        "id": changed.pop("id"),
        "type": table_name
    }

    return response, errors, code
