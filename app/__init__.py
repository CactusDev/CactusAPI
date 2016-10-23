""" Create the Flask instance """

from flask import Flask
from flask_restplus import Api
from . import resources

app = Flask(__name__, instance_relative_config=True)

app.config.from_object("config")

api = Api(app)
