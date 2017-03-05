import rethinkdb as rethink
import config
from jose import jwt
from uuid import UUID
from argon2 import PasswordHasher, exceptions
from datetime import datetime, timedelta
import logging as log
import argparse

ph = PasswordHasher()


def create_expires(days=0, hours=0, minutes=0, seconds=0, **kwargs):
    return int(datetime.timestamp(datetime.utcnow() + timedelta(
        days=days,
        hours=hours,
        minutes=minutes,
        seconds=seconds
    )))


def argon_hash(value):
    if not isinstance(value, str):
        raise TypeError("value must be type {}".format(str))

    return ph.hash(value)


def verify_password(password_hash, password):
    if not isinstance(password, str) or not isinstance(password_hash, str):
        raise TypeError("Password and hash must be type {}".format(str))
    try:
        return ph.verify(password_hash, password)
    except exceptions.VerificationError:
        return False


def update_record(table, data, conn):
    """Update a record in the DB"""
    record_id = data.pop("id")
    try:
        rethink.table(table).get(record_id).update(data).run(conn)
        return rethink.table(table).get(record_id).run(conn)
    except rethink.ReqlOpFailedError as e:
        return e


def create_record(table, data, conn):
    """Create a single record in the RethinkDB DB"""
    try:
        record = rethink.table(table).insert(data).run(conn)

        return rethink.table(table).get(
            record.get("generated_keys")[0]).run(conn)
    except rethink.ReqlOpFailedError as e:
        return e


def get_one(table, uid=None, conn=None, **kwargs):
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

    response = query.run(conn)

    if response is not None:
        if not is_uid:
            response = list(response)
        if len(response) > 0:
            return response[0]
        else:
            return dict(response)

    # No results!
    return {}


def generate_token(conn, password):
    user = get_one("users", token="root", conn=conn)

    if user == {}:
        raise LookupError
    else:
        hashed = user.get("password")
        exists = get_one("keys", token="root", conn=conn)

    try:
        ph.verify(hashed, password)
    except exceptions.VerifyMismatchError:
        raise ValueError

    scopes = "root"

    to_encode = {"scopes": scopes, "token": "root"}

    token = jwt.encode(to_encode, hashed, algorithm="HS512")
    key_store = {
        **to_encode,
        "expiration": create_expires(hours=4),
        "key": token
    }

    if exists == {}:
        create_record("keys", key_store, conn=conn)
    else:
        update_record("keys", {**exists, **key_store}, conn=conn)

    return token

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Generate the root token for the CactusAPI")

    parser.add_argument("--raw",
                        dest="raw", default=False, action="store_const",
                        const=True,
                        help="Make the script generate a token simply by the "
                        "password provided in the arguments, no prompt")
    parser.add_argument("password", type=str, metavar="password", nargs=1,
                        help="The root account's password")

    parsed = parser.parse_args()
    password = parsed.password[0]

    conn = rethink.connect(
        host=config.RDB_HOST,
        port=config.RDB_PORT,
        db="testing"
    )

    try:
        token = generate_token(conn, password)
    except ValueError as e:
        # It's the wrong password
        if not parsed.raw:
            print("\033[91mPASSWORD DOES NOT MATCH ROOT PASSWORD\033[0m")
        else:
            print("password")
    except LookupError as e:
        # DB doesn't have the root account in it
        if not parsed.raw:
            print("\033[91mROOT ACCOUNT IS NOT CONFIGURED\033[0m")
        else:
            print("account")
    else:
        if not parsed.raw:
            print("\033[92mKey:\n", token, "\033[0m")
        else:
            print(token)

    quit()
