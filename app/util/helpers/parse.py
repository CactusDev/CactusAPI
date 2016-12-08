from . import get_one


def validate_data(model, data):
    """
    Validates the provided data against the provided model
    Returns None if successful, a dict of errors if otherwise
    """
    errors = model.schema.validate(data)

    if errors != {}:
        return errors

    return None


def resource_exists(table_name, model, data, *args):
    # Dump to dict for searching
    parsed, errors, code = parse(model, data, partial=True)

    if errors is not None:
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
    errors = validate_data(model, data)

    # HACK: Need to figure out how to fix _schema: ["Invalid type"] error to
    # actually be more useful
    if errors is not None:
        if "_schema" in errors.get("response", {}):
            del errors["response"]["_schema"]
            errors["response"]["response"] = "Missing data for required field"

        # TODO: Make this return proper HTTP error codes
        # (should be fine, but just check)
        return None, errors, 400

    data, errors = model.schema.load(data, partial=partial)

    if errors != {}:
        return None, errors, 400

    dumped, errors = model.schema.dump(data)

    if errors != {}:
        return None, errors, 400

    return dumped, None, 200
