""" Create the Flask instance """

from flask import Flask

from flask_restplus import Api

app = Flask(__name__, instance_relative_config=True)

app.config.from_object("config")
api = Api(app)

from . import views
