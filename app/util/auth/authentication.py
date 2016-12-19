from argon2 import PasswordHasher, exceptions
from datetime import datetime, timedelta

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
