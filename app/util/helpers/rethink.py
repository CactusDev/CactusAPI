"""
Provides various helper functions for accessing RethinkDB

Beginnings of a super simple ORM of sorts
"""

# TODO: Implement exceptions instead of error return

import inspect
from html import unescape
from uuid import UUID, uuid4
import rethinkdb as rethink
from flask import g
from flask_restplus import fields

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


def exists(table, **kwargs):
    if not table.endswith('s'):
        table = table + 's'

    try:
        exists = list(rethink.table(table).filter(kwargs).run(g.rdb_conn))
        return len(exists) > 0
    except rethink.ReqlOpFailedError as e:
        return e


def update_record(table, data):
    """Update a record in the DB"""
    if not table.endswith('s'):
        table = table + 's'

    try:
        rethink.table(table).get(data["id"]).update(data).run(g.rdb_conn)

        return rethink.table(table).get(data["id"]).run(g.rdb_conn)
    except rethink.ReqlOpFailedError as e:
        return e


def create_record(table, data):
    """Create a single record in the RethinkDB DB"""
    if not table.endswith('s'):
        table = table + 's'

    try:
        record = rethink.table(table).insert(data).run(g.rdb_conn)

        return rethink.table(table).get(
            record.get("generated_keys")[0]).run(g.rdb_conn)
    except rethink.ReqlOpFailedError as e:
        return e


def get_one(table, uid=None, **kwargs):
    """ Get and return a single object from the given table via the UUID

    Returns None if there is nothing that matches

    Arguments:
        table:  String of the table objects are to be retrieved from
        uid:    A string of the object's UID if a specific row is required
                    Supplying this will ignore any keyword arguments given
        Other keyword arguments may be included filter the request by
    """

    if not isinstance(table, str):
        raise TypeError("table must be type str")

    if not table.endswith('s'):
        table = table + 's'

    # uid, if included, must be type string or uuid.UUID
    if uid is not None:
        if not isinstance(uid, str) and not isinstance(uid, UUID):
            return None

        # It's either type str or uuid.UUID, so we can continue on
        query = rethink.table(table).get(uid).limit(1)

    elif kwargs == {}:
        # uid was not included and neither were any kwargs
        # Select the first row in the table
        query = rethink.table(table).limit(1)

    elif kwargs != {}:
        # uid was not included, but there are kwargs
        query = rethink.table(table).filter(kwargs).limit(1)

    response = list(query.run(g.rdb_conn))
    if len(response) > 0:
        return response[0]

    return None


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
    elif limit is not None and kwargs == {}:
        query = rethink.table(table).limit(limit)
    elif limit is None and kwargs != {}:
        query = rethink.table(table).filter(kwargs)
    elif limit is None and kwargs == {}:
        query = rethink.table(table)

    return list(query.run(g.rdb_conn))
