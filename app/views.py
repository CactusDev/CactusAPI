"""Views for the API"""

import rethinkdb as rethink
import redis
from . import app
from flask import g, jsonify

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

prefix = app.config.get("API_PREFIX", "")

api.add_resource(resources.CommandList,
                 "{}/user/<string:token>/command".format(prefix))
api.add_resource(resources.CommandResource,
                 "{}/user/<string:token>/command/<command>".format(prefix))

api.add_resource(resources.TrustList,
                 "{}/user/<string:token>/trust".format(prefix))
api.add_resource(resources.TrustResource,
                 "{}/user/<string:token>/trust/<userId>".format(prefix))

api.add_resource(resources.QuoteList,
                 "{}/user/<string:token>/quote".format(prefix))
api.add_resource(resources.QuoteResource,
                 "{}/user/<string:token>/quote/<int:quoteId>".format(prefix))

api.add_resource(resources.RepeatList,
                 "{}/user/<string:token>/repeat".format(prefix))
api.add_resource(resources.RepeatResource,
                 "{}/user/<string:token>/repeat/<int:repeatId>".format(prefix))


from .util.auth import OAuthSignIn


@app.route("/authorize/<provider>")
def oauth_authorize(provider):
    """Authorize using oauth from the provided provider."""

    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@app.route("/callback/<provider>")
def oauth_callback(provider):
    """Callback for the provided provider."""

    oauth = OAuthSignIn.get_provider(provider)
    oauth_data = oauth.callback()

    return jsonify(oauth_data)
