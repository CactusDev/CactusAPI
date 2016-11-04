"""Views for the API"""

import rethinkdb as rethink
import redis
import remodel
from . import app
from flask import g
from flask_restplus import reqparse

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
    g.parser = reqparse.RequestParser()
