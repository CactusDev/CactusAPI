""" Create the Flask instance """

from flask import Flask

from flask_restplus import Api
from flask_limiter import Limiter, util
from raven.contrib.flask import Sentry

app = Flask(__name__, instance_relative_config=True)

app.config.from_object("config")
api = Api(app)

limiter = Limiter(app, key_func=util.get_remote_address)

if app.config["SENTRY_ACTIVE"]:
    sentry = Sentry(app, dsn=app.config["SENTRY_DSN"])

from . import views
