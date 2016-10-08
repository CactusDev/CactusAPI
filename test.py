"""
Foo bar
"""

import inspect
from uuid import uuid4
from pprint import pprint
import models
import rethinkdb as rethink
from helpers import generate_packet, generate_error

ENDPOINTS = ["friend", "user", "message"]

PATH = "/api/v1/channel/paradigmshift3d/friend"

MODEL = "friend"

METHOD = "GET"
USER = "paradigmshift3d"

RDB_CONN = rethink.connect(host="localhost",
                           db="cactus")

DATA = list(rethink.table(MODEL + "s").run(RDB_CONN))

if DATA == []:
    print("ERRORS AND DOOM!")
    error_packet, errors = generate_error(
        uid=uuid4(),
        status="404",
        code="405",
        title="Table does not have any entries",
        detail="Friends table does not have any entries",
        source={"pointer": PATH})

    if errors is not None:
        print("Errors happened when making the error packet!")
        print(errors)
    else:
        print({"errors": [error_packet]})

POST_IGNORE = []

# Remove the ignored keys
for name, obj in inspect.getmembers(models):
    if name.lower() == MODEL:
        for foo in DATA:
            POST_IGNORE.append(
                {key: foo[key] for key in foo if key not in obj.ignore})

        relationships = [
            relationship.lower() for relationship in obj.belongs_to]
        relationships.extend([relate.lower() for relate in obj.has_one])
        relationships.extend([relate.lower() for relate in obj.has_many])
        relationships.extend([
            relate.lower() for relate in obj.has_and_belongs_to_many])

# Generate the final packet
PACKET = [generate_packet(
    MODEL,
    uuid4(),
    data,
    PATH,
    relationships
) for data in POST_IGNORE]

pprint(PACKET)
