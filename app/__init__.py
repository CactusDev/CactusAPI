""" Create the Flask instance """

from flask import Flask
from flask_restplus import Api

app = Flask(__name__, instance_relative_config=True)

app.config.from_object("config")
API = Api()
API.init_app(app)

from . import views

API.add_resource(views.resources.CommandResource, "/command")
