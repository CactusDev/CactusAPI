""" Create the Flask instance """

from flask import Flask

from flask_restplus import Api

app = Flask(__name__, instance_relative_config=True)

app.config.from_object("config")

from . import views

api = Api(app)

from . import resources

api.add_resource(resources.CommandList,
                 "/channel/<token>/command")
api.add_resource(resources.CommandResource,
                 "/channel/<token>/command/<command>")
