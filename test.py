from helpers import *
import rethinkdb as rethink
import models
import inspect

endpoints = ["friend", "user", "message"]

path = "/api/v1/channel/paradigmshift3d/friend"

model = "friend"

method = "GET"
user = "paradigmshift3d"

rdb_conn = rethink.connect(host="localhost",
                             db="cactus")

data = list(rethink.table(model + "s").run(rdb_conn))

print(data)

# Remove the ignored keys
for name, obj in inspect.getmembers(models):
    if name.lower() == model:
        for foo in data:
            print({key: foo[key] for key in foo if key not in obj.ignore})
