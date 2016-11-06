"""Views for the API"""

import rethinkdb as rethink
import redis
import remodel
from . import app
from flask import g

remodel.connection.pool.configure(db=app.config["RDB_DB"],
                                  host=app.config["RDB_HOST"],
                                  port=app.config["RDB_PORT"])
REDIS_CONN = redis.Redis()


@app.before_request
def before_request():
    """Make certain things accessible in every new request"""
    g.rdb_conn = rethink.connect(host=app.config["RDB_HOST"],
                                 port=app.config["RDB_PORT"],
                                 db=app.config["RDB_DB"])

    g.redis = redis.Redis()

from . import api
from . import resources

api.add_resource(resources.CommandList, "/user/<string:token>/command")
api.add_resource(resources.CommandResource,
                 "/user/<string:token>/command/<command>")
api.add_resource(resources.TrustList, "/user/<string:token>/trust")
api.add_resource(resources.TrustResource,
                 "/user/<string:token>/trust/<string:userName>")
