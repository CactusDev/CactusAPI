import rethinkdb as rethink

from .rethink import (get_one, get_all, get_multiple, get_random, create_record,
                      update_record)
from .parse import parse, validate_data, resource_exists, convert
from .response import humanize_datetime, json_api_response


def _update(table_name, data, update_id):

    changed = update_record(
        table_name, {**data, "id": update_id})
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


def check_existance(table_name, **kwargs):
    exist_filter = {key: value for
                    key, value in kwargs.items()
                    if key != "post" and
                    (isinstance(value, (str, int)) or key == "cased")}

    if kwargs.get("cased"):
        exist_filter = {**kwargs, "cased": kwargs["cased"]}
        if "post" in exist_filter:
            del exist_filter["post"]

    # kwargs is the data we're using to check if the resource exists off of
    exists_or_error, code = resource_exists(table_name, **exist_filter)

    if kwargs.get("post", False) and code == 200:
        return "Resource already exists", 409

    # Parse the results
    if isinstance(exists_or_error, list) and len(exists_or_error) > 0:
        exists_or_error = exists_or_error[0]

    return exists_or_error, code


def create_or_update(table_name, model, data, **kwargs):

    exists_or_error, code = check_existance(table_name, **kwargs)

    # Resource exists - update and return response
    if code == 200:
        parsed, errors, code = parse(model, data, partial=True)
        if errors != {}:
            return {}, errors, code

        changed, code = _update(table_name, parsed, exists_or_error["id"])
        try:
            response = json_api_response(changed, table_name, model)
        except TypeError as e:
            return {}, e.args, 500

        return response, errors, code

    # Resource does NOT exist - create resource & return results
    elif code == 404:
        parsed, errors, code = parse(model, data)
        if errors != {}:
            return {}, errors, code

        changed, code = _create(table_name, model, parsed)

        try:
            response = json_api_response(changed, table_name, model)
        except TypeError as e:
            return {}, e.args, 500

        return response, errors, code

    # Some other number, thus an error
    else:
        return {}, exists_or_error, code


def update_resource(table_name, model, data, **kwargs):
    errors = validate_data(model, data, partial=True)
    if errors is not None:
        return {}, errors, 400

    exists_or_error, code = resource_exists(table_name, **kwargs)
    # There was an error during pre-parsing, return that
    if code != 200:
        return {}, exists_or_error, code

    data["id"] = exists_or_error["id"]

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
