"""Views for the API"""

import rethinkdb as rethink
import redis
import remodel
from app import app
from flask import g

remodel.connection.pool.configure(db=app.config["RDB_DB"],
                                  host=app.config["RDB_HOST"],
                                  port=app.config["RDB_PORT"])
REDIS_CONN = redis.Redis()


@app.before_request
def before_request():
    """Set the Flask session object's user to Flask-Login's current_user"""
    g.rdb_conn = rethink.connect(host=app.config["RDB_HOST"],
                                 port=app.config["RDB_PORT"],
                                 db=app.config["RDB_DB"])

    g.redis = redis.Redis()
