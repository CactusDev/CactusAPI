import rethinkdb as rethink

from .rethink import (get_one, get_all, get_multiple, get_random, create_record,
                      update_record)
from .parse import parse, validate_data, resource_exists
from .response import humanize_datetime, json_api_response


def create_or_update(table_name, model, data, *args, **kwargs):
    """Takes the provided data and creates or edits the resource"""
    # Check if the resource exists based on the string args given
    exist_check = {key: data[key] for key in args if isinstance(key, str)}
    exists_or_error, code = resource_exists(table_name, model, **exist_check)

    # There was an error during pre-parsing, return that
    if code == 400:
        return {}, exists_or_error, code

    if exists_or_error != {}:
        update_id = exists_or_error["id"]
        parsed, errors, code = parse(model, data, partial=True)
        if errors != {}:
            return {}, errors, code
        else:
            # Don't change the createdAt
            if parsed.get("createdAt", None) is not None:
                del parsed["createdAt"]

            changed = update_record(table_name, {**parsed, "id": update_id})
            code = 200
    else:
        for (key, skey) in model.force_on_create.items():
            print(data.get(key, None))
            if data.get(key, None) is not None:
                if data[key].get(skey, None) is None:
                    message = "A valid {} object must be provided during {} "\
                        "creation".format(skey, table_name)

                    return {}, {key: {skey: message}}, 400

        parsed, errors, code = parse(model, data)
        if errors != {}:
            return {}, errors, code
        else:
            changed = create_record(table_name, parsed)
            code = 201

    if isinstance(changed, Exception):
        return {}, {"errors": changed.args}, 500

    # Try-except because json_api_response throws errors if stuff is bad
    try:
        return json_api_response(changed, table_name), {}, code
    except TypeError as e:
        return {}, {"errors": e.args}, 400


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

    # Try-except because json_api_response throws errors if stuff is bad
    try:
        return json_api_response(changed, table_name), {}, code
    except TypeError as e:
        return {}, {"errors": e.args}, 400
