""" Create the Flask instance """

from flask import Flask

from flask_restplus import Api
from flask_limiter import Limiter, util

app = Flask(__name__, instance_relative_config=True)

app.config.from_object("config")
api = Api(app)

limiter = Limiter(app, key_func=util.get_remote_address)

from . import views
