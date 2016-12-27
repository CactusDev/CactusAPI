import rethinkdb as rethink

from .rethink import (get_one, get_all, get_multiple, get_random, create_record,
                      update_record)
from .parse import parse, validate_data, resource_exists, convert
from .response import humanize_datetime, json_api_response


def _update(table_name, model, data, update_id):
    parsed, errors, code = parse(model, data, partial=True)
    if errors != {}:
        return errors, code
    else:
        changed = update_record(
            table_name, {**parsed, "id": update_id})
        code = 200

    return changed, code


def _create(table_name, model, data):
    if hasattr(model, "force_on_create"):
        if isinstance(model.force_on_create, dict):
            for (key, skey) in model.force_on_create.items():
                if data.get(key, None) is not None:
                    if data[key].get(skey, None) is None:
                        message = "A valid {} object must be provided during"\
                            " {} creation".format(skey, table_name)

                        return {key: {skey: message}}, 400

        elif isinstance(model.force_on_create, set):
            for key in model.force_on_create:
                if data.get(key) is None:
                    message = "A valid {} must be provided during {} creation"\
                        "".format(key, table_name)

                    return {key: message}, 400

    parsed, errors, code = parse(model, data)
    if errors != {}:
        return errors, code
    else:
        changed = create_record(table_name, parsed)
        code = 201

    return changed, code


def _check_exist(table_name, model, data, *args):
    if not set(args).issubset(set(data.keys())):
        return {
            "errors": [
                "Missing required key '{}'".format(key)
                for key in args if key not in data.keys()]
        }, 400

    # Check if the resource exists based on the string args given
    exist_check = {key: data[key] for key in args if isinstance(key, str)}
    exists_or_error, code = resource_exists(table_name, model, **exist_check)

    return exists_or_error, code


def create_or_update(table_name, model, data, *args, **kwargs):
    """Takes the provided data and creates or edits the resource"""
    exists_or_error, code = _check_exist(table_name, model, data, *args)

    if code == 400:
        return {}, exists_or_error, code

    if code is None:
        if kwargs.get("post", False):
            # Try-except because json_api_response throws errors if stuff is
            # bad
            try:
                return json_api_response(exists_or_error, table_name, model), {}, 409
            except TypeError as e:
                return {}, {"errors": e.args}, 400

        update_id = exists_or_error["id"]

        # Don't change the createdAt
        if data.get("createdAt") is not None:
            del data["createdAt"]
        # Don't let users change counts
        if data.get("count") is not None:
            del data["count"]

        changed, code = _update(table_name, model, data, update_id)

        # Update was not succesful
        if code != 200:
            changed = convert(changed)
            return {}, changed, code

    elif code == 404:
        # Don't change the createdAt
        if data.get("createdAt") is not None:
            del data["createdAt"]
        # Don't let users change counts
        if data.get("count") is not None:
            del data["count"]

        changed, code = _create(table_name, model, data)

        # Creation didn't succesfully complete!
        if code != 201:
            changed = convert(changed)
            return {}, changed, code

    if isinstance(changed, Exception):
        return {}, {"errors": changed.args}, 500

    # Try-except because json_api_response throws errors if stuff is bad
    try:
        return json_api_response(changed, table_name, model), {}, code
    except TypeError as e:
        return {}, {"errors": e.args}, 400


def update_resource(table_name, model, data, **kwargs):
    errors = validate_data(model, data, partial=True)
    if errors is not None:
        return {}, errors, 400

    exists_or_error, code = resource_exists(table_name, model, **kwargs)
    data["id"] = exists_or_error["id"]

    # There was an error during pre-parsing, return that
    if code is not None:
        return {}, exists_or_error, code

    if exists_or_error is not None:
        # Don't change the createdAt
        if exists_or_error.get("createdAt", None) is not None:
            del exists_or_error["createdAt"]

    try:
        changed = update_record(
            table_name, {**data, "id": exists_or_error["id"]})
        code = 200
    except rethink.ReqlOpFailedError as e:
        return {}, {"errors": e.args}, 500

    # Try-except because json_api_response throws errors if stuff is bad
    try:
        return json_api_response(changed, table_name, model), {}, code
    except TypeError as e:
        return {}, {"errors": e.args}, 400
