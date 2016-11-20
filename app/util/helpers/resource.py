from . import (get_one, create_record, update_record,
               humanize_datetime, get_all, get_multiple)


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
        parsed = humanize_datetime(parsed, ["createdAt"])
        response.append({
            "id": parsed.pop("id"),
            "attributes": parsed,
            "type": table_name
        })
        if err != {}:
            errors.append(err)

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


def create_or_none(table_name, model, data, filter_keys, **kwargs):

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
