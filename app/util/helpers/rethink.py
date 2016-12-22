"""
Provides various helper functions for accessing RethinkDB

Beginnings of a super simple ORM of sorts
"""

from uuid import UUID, uuid4
import rethinkdb as rethink
from flask import g
from flask_restplus import fields

from .decorators import pluralize_arg

META_CREATED = {
    "created": True,
    "updated": False
}

META_EDITED = {
    "created": False,
    "updated": True
}


@pluralize_arg
def next_numeric_id(table, *, id_field, **kwargs):
    try:
        count = list(rethink.table(table).filter(kwargs).run(g.rdb_conn))
        new_id = 0
        for record in count:
            if id_field in record and record[id_field] >= new_id:
                new_id = record[id_field] + 1

        return new_id
    except rethink.ReqlOpFailedError as e:
        return e


@pluralize_arg
def exists(table, **kwargs):
    """
    Checks if the number of results returned for the query is 1 or greater.
    """
    try:
        exists = list(rethink.table(table).filter(kwargs).run(g.rdb_conn))
        return len(exists) > 0
    except rethink.ReqlOpFailedError as e:
        return e


@pluralize_arg
def update_record(table, data):
    """Update a record in the DB"""
    record_id = data.pop("id")
    try:
        rethink.table(table).get(record_id).update(data).run(g.rdb_conn)

        return rethink.table(table).get(record_id).run(g.rdb_conn)
    except rethink.ReqlOpFailedError as e:
        return e


@pluralize_arg
def create_record(table, data):
    """Create a single record in the RethinkDB DB"""
    try:
        record = rethink.table(table).insert(data).run(g.rdb_conn)

        return rethink.table(table).get(
            record.get("generated_keys")[0]).run(g.rdb_conn)
    except rethink.ReqlOpFailedError as e:
        return e


@pluralize_arg
def delete_record(table, limit=1, **kwargs):
    """
    Delete a record in the DB
    Returns the UUID of the record deleted, or None if it fails
    """
    try:
        response = []
        if limit is None:
            request = rethink.table(table).filter(kwargs)
        elif isinstance(limit, int):
            request = rethink.table(table).filter(kwargs).limit(limit)

        results = list(request.run(g.rdb_conn))

        if len(results) > 0:
            for record in results:
                deleted = rethink.table(table).get(
                    record["id"]
                ).delete().run(g.rdb_conn)

                if deleted["deleted"] > 0:
                    response.append(record["id"])

            return response

    except rethink.ReqlOpFailedError as e:
        return e

    return None


@pluralize_arg
def get_one(table, uid=None, **kwargs):
    """ Get and return a single object from the given table via the UUID

    Returns None if there is nothing that matches

    Arguments:
        table:  String of the table objects are to be retrieved from
        uid:    A string of the object's UID if a specific row is required
                    Supplying this will ignore any keyword arguments given
        Other keyword arguments may be included filter the request by
    """
    is_uid = False

    # uid, if included, must be type string or uuid.UUID
    if uid is not None:
        if not isinstance(uid, str):
            if not isinstance(uid, UUID):
                raise TypeError("uid must be type {} or {}".format(str, UUID))
            else:
                uid = uid.hex

        # It's either type str or uuid.UUID, so we can continue on
        query = rethink.table(table).get(uid)
        is_uid = True

    elif kwargs == {} and uid is None:
        # uid was not included and neither were any kwargs
        # Select the first row in the table
        query = rethink.table(table).limit(1)

    elif kwargs != {} and uid is None:
        # uid was not included, but there are kwargs
        query = rethink.table(table).filter(kwargs).limit(1)

    response = query.run(g.rdb_conn)

    if response is not None:
        if not is_uid:
            response = list(response)
            if len(response) > 0:
                return response[0]
        else:
            return dict(response)

    # No results!
    return {}


@pluralize_arg
def get_random(table, *, limit, **kwargs):
    try:
        return rethink.table(
            table).filter(kwargs).sample(limit).run(g.rdb_conn)
    except rethink.ReqlOpFailedError as e:
        return e


@pluralize_arg
def get_all(table, **kwargs):
    """ Get and retrieve all rows in the provided table

    A wrapper for retrieve_multiple() to provide more functionality

    Raises a TypeError if table is not type str

    Arguments:
        table:  String of the table objects are to be retrieved from
        Other keyword arguments may be included to filter the request by
    """
    return get_multiple(table, **kwargs)


@pluralize_arg
def get_multiple(table, limit=None, **kwargs):
    """ Get and return multiple rows in the provided table in list form

    Raises a TypeError if table is not type str

    Arguments:
        table:  String of the table objects are to be retrieved from
        limit:  Int of the total number of objects wished to be returned
        Other keyword arguments may be included filter the request by
    """

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
