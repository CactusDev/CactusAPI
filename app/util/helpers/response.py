from datetime import datetime
from dateutil import parser


def json_serialize(obj):
    """
    Takes a datetime.datetime object and makes it serializable by converting
    it to an ISO-8601 string.
    """
    if isinstance(obj, datetime):
        return obj.isoformat()

    return None


def humanize_datetime(to_humanize, args):
    """
    Takes a marshalled JSON dict and a list of args to check and converts
    those keys into human-readable datetimes
    """
    if not isinstance(args, list):
        raise TypeError("args must be a list of strings")

    for key in args:
        if not isinstance(key, str):
            raise TypeError("args must be a list of strings")
        # If the key exists, then convert it from the RethinkDB format to the
        # more human-readable date & time representation
        humanize = to_humanize.get(key, None)
        if humanize is not None:
            to_humanize[key] = parser.parse(humanize).strftime("%c")

    return to_humanize
