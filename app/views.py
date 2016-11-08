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

prefix = app.config["API_PREFIX"]

api.add_resource(resources.CommandList,
                 "{}/user/<string:token>/command".format(prefix))
api.add_resource(resources.CommandResource,
                 "{}/user/<string:token>/command/<command>".format(prefix))
api.add_resource(resources.TrustList,
                 "{}/user/<string:token>/trust".format(prefix))
api.add_resource(resources.TrustResource,
                 "{}/user/<string:token>/trust/<userName>".format(prefix))
api.add_resource(resources.QuoteList,
                 "{}/user/<string:token>/quote".format(prefix))
api.add_resource(resources.QuoteResource,
                 "{}/user/<string:token>/quote/<int:quoteId>".format(prefix))
