"""Views for the API"""

import rethinkdb as rethink
import redis
from . import app
from flask import g, jsonify, request

REDIS_CONN = redis.Redis()


@app.before_request
def before_request():
    """Make certain things accessible in every new request"""
    g.rdb_conn = rethink.connect(host=app.config["RDB_HOST"],
                                 port=app.config["RDB_PORT"],
                                 db=app.config["RDB_DB"],
                                 user=app.config["RDB_USERNAME"],
                                 password=app.config["RDB_PASSWORD"])

    g.redis = redis.Redis()

from . import api
from . import resources
from . import authentication


prefix = app.config.get("API_PREFIX", "")

api.add_resource(resources.CommandList,
                 "{}/user/<string:token>/command".format(prefix))
api.add_resource(resources.CommandResource,
                 "{}/user/<string:token>/command/<name>".format(prefix))
api.add_resource(resources.CommandCounter,
                 "{}/user/<string:token>/command/<name>/count".format(prefix))

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
                 "{}/user/<string:token>/repeat/<repeatName>".format(prefix))

api.add_resource(resources.AliasResource,
                 "{}/user/<string:token>/alias/<name>".format(prefix))

api.add_resource(resources.SocialList,
                 "{}/user/<string:token>/social".format(prefix))
api.add_resource(resources.SocialResource,
                 "{}/user/<string:token>/social/<service>".format(prefix))

# Disabled because of security reasons, don't necessarilly need it
# api.add_resource(resources.UserList,
#                  "{}/user".format(prefix))
api.add_resource(resources.UserResource,
                 "{}/user/<string:userName>".format(prefix))

api.add_resource(resources.ConfigResource,
                 "{}/user/<string:token>/config".format(prefix))

api.add_resource(resources.PointResource,
                 "{}/user/<string:token>/points/<string:name>".format(prefix))

# API Login endpoint
api.add_resource(authentication.Login, "{}/login".format(prefix))

from .util.auth import OAuthSignIn
from . import util
from . import models


@app.route("/test/<token>/<name>")
def test(**kwargs):
    resp, err, code = util.helpers.create_or_update(
        "commands", models.Command, {**request.get_json(), **kwargs}, "name", **kwargs)

    return jsonify({"resp": resp, "err": err}), code


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
