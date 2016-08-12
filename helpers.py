"""
Provides various helper functions for accessing RethinkDB

Beginnings of a super simple ORM of sorts
"""

from uuid import UUID
import rethinkdb as rethink
from flask import g


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
        query = rethink.table(table).filter({id: uid})

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
