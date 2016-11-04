from datetime import datetime
from flask import g, request

from flask_restplus import marshal
from marshmallow import Schema

from ... import models

from . import get_one, create_record, update_record, humanize_datetime, exists


def parse(model, data):

    errors = model.schema.validate(data)
    if errors:
        return {"errors": [errors]}, 500

    response, meta = model.schema.dump(model(**data))

    return response, meta, 200


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
        changed = update_record(
            table_name, {**parsed, "id": exists["id"]})
        code = 200
    else:
        changed = create_record(table_name, parsed)
        code = 201

    if isinstance(changed, Exception):
        return {"errors": changed.args}, 500

    elif code == 201:
        parsed = get_one(table_name, uid=changed)
        # TODO: Deal with None response, which shouldn't happen

    response = humanize_datetime(parsed, ["createdAt"])

    response = {
        "id": response.pop("id"),
        "attributes": response,
        "type": table_name
    }

    return response, errors, code
