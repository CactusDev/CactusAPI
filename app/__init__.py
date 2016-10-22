""" Create the Flask instance """

from flask import Flask
from flask_restplus import Api, Resource
from . import resources

app = Flask(__name__, instance_relative_config=True)

app.config.from_object("config")
api = Api(app)

api.add_resource(resources.CommandResource, "/command")
api.add_resource(resources.QuoteResource, "/quote")
