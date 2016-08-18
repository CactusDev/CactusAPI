"""
Provides various helper functions for accessing RethinkDB

Beginnings of a super simple ORM of sorts
"""

# TODO: Implement exceptions instead of error return

import inspect
from uuid import UUID, uuid4
import rethinkdb as rethink
from flask import g
import models

META_CREATED = {
    "created": True,
    "updated": False
}

META_EDITED = {
    "created": False,
    "updated": True
}


def retrieve_user(username):
    """
    Get and return a user

    Searches the 'users' table case-insensitive
    """
    user = rethink.table("users").filter(
        lambda user:
        user["userName"].match("(?i){}".format(str(username)))
    ).limit(1).run(g.rdb_conn)

    return list(user)


def get_single(table, uid=None, **kwargs):
    """ Get and return a single object from the given table via the UUID

    Returns None if table is not type str

    Arguments:
        table:  String of the table objects are to be retrieved from
        uid:    A string of the object's UID if a specific row is required
                    Supplying this will ignore any keyword arguments given
        Other keyword arguments may be included filter the request by
    """

    if not isinstance(table, str):
        return None

    # uid, if included, must be type string or uuid.UUID
    if uid is not None:
        if not isinstance(uid, str) and not isinstance(uid, UUID):
            return None

        # It's either type str or uuid.UUID, so we can continue on
        query = rethink.table(table).filter({"id": uid})

    elif kwargs == {}:
        # uid was not included and neither were any kwargs
        # Select the first row in the table
        query = rethink.table(table).limit(1)

    elif kwargs != {}:
        # uid was not included, but there are kwargs
        query = rethink.table(table).filter(kwargs).limit(1)

    return list(query.run(g.rdb_conn))


def get_all(table, **kwargs):
    """ Get and retrieve all rows in the provided table

    A wrapper for retrieve_multiple() to provide more functionality

    Returns None if table is not type str

    Arguments:
        table:  String of the table objects are to be retrieved from
        Other keyword arguments may be included to filter the request by
    """

    return get_multiple(table, **kwargs) if isinstance(table, str) else None


def get_multiple(table, limit=None, **kwargs):
    """ Get and return multiple rows in the provided table in list form

    Returns None if table is not type str

    Arguments:
        table:  String of the table objects are to be retrieved from
        limit:  Int of the total number of objects wished to be returned
        Other keyword arguments may be included filter the request by
    """

    if not isinstance(table, str):
        return None

    # Check if limit is not None, then the user wants a limit

    if limit is not None and kwargs != {}:
        query = rethink.table(table).filter(kwargs).limit(limit)
    elif limit is None and kwargs != {}:
        query = rethink.table(table).filter(kwargs)
    elif limit is not None and kwargs == {}:
        query = rethink.table(table).limit(limit)

    return list(query.run(g.rdb_conn))


def generate_error(meta=None, **kwargs):
    """Create and return a JSON-API compliant error packet

    All parameters are optional

    Parameters:
        uid:            Unique ID for this individual error
        links:          An object containing an about key that is a link that
                            leads to further details about this particular
                            occurrence of the problem.
        status:         the HTTP status code applicable to this problem,
                            expressed as a string value.
        code:           an application-specific error code, a string value.
        title:          Short, human-readable summary of the problem.
                            SHOULD NOT CHANGE between occurences of problem
        detail:         Human-readable explanation specific to this problem
        source:         An object containing references to the source of the
                            error
        meta:           Dict of meta information, NOT required
    """

    packet = {}
    errors = {}

    correct_types = {
        "uid": None,
        "links": dict,
        "status": str,
        "code": str,
        "title": str,
        "detail": str,
        "source": dict,
        "meta": dict
    }

    # Remove any non-standard arguments
    packet = {key: kwargs[key] for key in kwargs if key in correct_types}

    # Check all of the included arguments are of the proper type
    for arg in packet:
        if correct_types[arg] is not None and \
                not isinstance(packet[arg], correct_types[arg]):
            errors[arg] = "incorrect type {}, should be type {}".format(
                arg.__class__.__name__, correct_types[arg].__name__
                )

    if "links" in packet:
        if "about" in packet["links"]:
            if not isinstance(packet["links"]["about"], str):
                errors["links:about"] = "link 'about' key is not a string"
        else:
            errors["links"] = "link key does not contain required 'about' key"

    if "source" in packet and not isinstance(packet["source"], dict):
        errors["source"] = "'source' key is not a dict"

    if meta is not None and isinstance(meta, dict):
        packet["meta"] = meta

    return (packet, None) if len(errors) == 0 else (None, errors)


def generate_packet(packet_type, uid, attributes, path, relationships,
                    meta=None):
    """Create and return a packet.

    Parameters:
        packet_type:    String of object type being returned
        uid:            ID of whatever is being returned
        attributes:     Dict of data attributes to return
                            MUST include a "user" key
        path:           String of endpoint being accessed for link generation
        relationships:  A list of all endpoints that the resource is related to
        meta:           Dict of meta information, not required
    """

    user = attributes["userName"] if "userName" in attributes else None

    print("id:    ", uid)
    print("\ttype:\t", packet_type)
    print("\tattr:\t", attributes)
    print("\tpath:\t", path)
    print("\tuser:\t", user)

    link_base = "/api/v1/user/{}".format(user.lower())

    # TODO: Add code that creates relationships for messages/channel-level

    relationship_return = {key: {
        "links": {
            "self": "{}/relationships/{}".format(link_base, str(key)),
            "related": "{}/{}".format(link_base, str(key))
        }
    } for key in relationships if key != str(packet_type) and user is not None}

    to_return = {
        "data": {
            "type": str(packet_type),
            "id": str(uid),
            "attributes": attributes,
            "relationships": relationship_return,
            "jsonapi": {
                "version": "1.0"
            },
            "links": {
                "self": str(path)
            }
        }
    }

    if meta is not None and isinstance(meta, dict):
        to_return["meta"] = meta

    return to_return


def create_resource(model, fields):
    """
    Creates a new resource

    Arguments:
        model:      The model for the resource to be created
        fields:     The data to fill the object with
    """

    errors = {}

    for name, obj in inspect.getmembers(models):

        # Does the current object's name match the resource we're on?
        if name.lower() == model:

            does_exist = list(
                rethink.table(
                    name.lower() + "s"
                ).filter(fields).limit(1).run(g.rdb_conn)
            )

            if does_exist:
                return does_exist, None

            # Yes it does, let's make the new resource
            # Sort the parameters included by obj.fields

            if fields is not None:
                check = {key: fields[key] for key in fields if
                         key in obj.fields}

                for field in obj.fields:
                    if field in check:
                        if not isinstance(check[field],
                                          obj.fields[field]["type"]):
                            errors[field] = {
                                "detail": "Field is incorrect type '{}'."
                                          " Should be '{}'".format(
                                              type(check[field]),
                                              obj.fields[field]["type"]
                                          ),
                                "title": "Field is incorrect type",
                                "code": "102"
                            }

                    elif "default" in obj.fields[field]:
                        check[field] = obj.fields[field]["default"]

                    else:
                        errors[field] = {
                            "detail": "Required field {} not included".format(
                                field
                            ),
                            "title": "Required field is not included",
                            "code": "103"
                            }

            if check.keys() == obj.fields.keys() and errors == {}:
                # The fields for the new object match the schema
                # Create the new object
                created = obj(
                    **fields
                )
                created.save()

                data = get_single(model + "s", uid=created["id"])

    return data, True if errors == {} else errors, False


def generate_response(model, path, method, params, data=None):
    """
    Generates and returns the required response packet(s)

    Arguments:
        model:      The database model that is being accessed
        path:       The endpoint's path
        method:     The HTTP request's method, decides if editing or just
                        retrieving results
        params:     The HTTP request parameters in dict form
        data:       Optional, the data retrieved from the database. If not
                        included everything will be retrieved for the model
    """
    print(method)

    model_dict = {name.lower(): obj for
                  name, obj in inspect.getmembers(models)}
    errors = {}

    if model not in model_dict:
        return {"error": "Field '{}' not in defined models".format(model)}, 404

    # Make sure we have the data we need
    if method == "GET":
        if data is None:
            # Retrieve everything in the table
            data = list(rethink.table(model + "s").run(g.rdb_conn))

    elif method in ["PATCH", "POST"]:
        # Create/edit a new object
        if "id" in params:
            # Retrieve a specific row
            data = get_single(model, uid=params["id"])

        if method == "POST":
            # Specifically create a new resource
            data, created = create_resource(model, data)

            if created is False:
                # It's an error
                errors = data
            elif created is True:
                meta = META_CREATED

        elif method == "PATCH":
            # record editing/creation
            if data is not None:
                check = {key: data[key] for key in
                         data if key in obj.fields}

                for field in check:
                    if not isinstance(check[field], obj.data[field]["type"]):
                        errors[field] = {
                            "title": "Field is incorrect type",
                            "detail": "Field is incorrect type '{}'."
                                      "Should be '{}'".format(
                                          type(check[field]),
                                          obj.fields[field]["type"]
                                       ),
                            "code": "102"
                        }

    elif method == "DELETE":
        # Some data is required
        data = list(rethink.table(model + "s").filter(
            data
        ).limit(1).run(g.rdb_conn))[0]

        print("377:\t", data)

        if data != []:
            success = rethink.table(model + "s").get(
                data["id"]).delete().run(g.rdb_conn)

            print(success)

            return {"deleted": data["id"], "success": True}, 200
        else:
            return {
                "deleted": None,
                "success": False
            }, 500

    if errors != {}:
        [generate_error(
            uid=uuid4(),
            source={"pointer": path},
            **errors[error]
        ) for error in errors]

    if data == [] and errors == {}:
        print("ERRORS AND DOOM!")
        error_packet, errors = generate_error(
            uid=uuid4(),
            status="404",
            code="405",
            title="Table does not have any entries",
            detail="Friends table does not have any entries",
            source={"pointer": path}
        )

        if errors is not None:
            print("Errors occured while generating the error packet!")
            return {"errors": [error_packet]}, 500
        else:
            return {"errors": [error_packet]}, 404

    # List to hold all data after ignored fields are removed
    post_ignore = []

    for name, obj in inspect.getmembers(models):
        # Does the current object's name match the resource we're on?
        if name.lower() == model:
            # Yes, continue on with the code
            if isinstance(data, list):
                for row in data:
                    print(row)
                    post_ignore.append(
                        {key: row[key] for
                         key in row if
                         key not in obj.ignore}
                    )
            else:
                post_ignore.append(
                    {key: data[key] for
                     key in data if
                     key not in obj.ignore}
                )

            relationships = [
                relationship.lower() for relationship in obj.belongs_to]
            relationships.extend([relate.lower() for relate in obj.has_one])
            relationships.extend([relate.lower() for relate in obj.has_many])
            relationships.extend([
                relate.lower() for relate in obj.has_and_belongs_to_many])

    to_return = [generate_packet(
        model,
        uuid4(),
        data,
        path,
        relationships,
    ) for data in post_ignore]

    # Return the response in JSON form, with proper success code
    return to_return, 200
