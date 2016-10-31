from datetime import datetime
from flask import g

from flask_restplus import marshal

from ..models import fields_map
from ..util import helpers
# TODO: Convert all these as resp_helpers, r_helpers, etc. to single helpers
from ..util import response_helpers as resp_helpers


def parse(model):
    defaults = {}

    for field in model.model.items():
        name = field[1].__class__.__name__.lower()
        check = fields_map.get(name, None)
        default = getattr(field[1], "default", None)
        if default is None:
            if check is not None:
                g.parser.add_argument(field[0], required=True, type=check)
            else:
                g.parser.add_argument(field[0])
        else:
            defaults[field[0]] = default

    response = g.parser.parse_args()


def create(table_name, model):

    # Parse the data from the request and take care of defaults
    response = parse(model)

    # Interact with RethinkDB and create the new record
    created = helpers.create_record(table_name, response)

    if isinstance(created, Exception):
        return {"errors": created.args}, 500

    response = marshal({**response, **defaults}, model.model)
    response = resp_helpers.humanize_datetime(response, ["createdAt"])

    return response, 200
