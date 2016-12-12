"""Config resource"""

from flask import request

from flask_restplus import Resource, marshal

from ..models import Config
from ..schemas import ConfigSchema
from ..util import helpers

# TODO: Solve createdAt cannot be formatted as datetime bug


class ConfigResource(Resource):

    @helpers.lower_kwargs("token")
    def get(self, path_data, **kwargs):
        attributes, errors, code = helpers.single_response(
            "config", Config, **path_data)

        response = {}

        if errors != []:
            response["errors"] = errors
        else:
            response["data"] = attributes

        return response, code

    @helpers.lower_kwargs("token")
    def patch(self, path_data, **kwargs):
        json_data = request.get_json()

        if json_data is None:
            return {"errors": ["Bro...no data"]}, 400

        data = {**json_data, **path_data}

        # TODO: Need to add ability to just edit because EXPLOSIONS probs
        # for sure gonna happen
        attributes, errors, code = helpers.update_resource(
            "config", Config, data, "token"
        )

        response = {}

        if code == 201:
            response["meta"] = {"created": True}
        elif code == 200:
            response["meta"] = {"edited": True}

        if errors == {}:
            response["data"] = attributes
        else:
            response["errors"] = errors

        return response, code
