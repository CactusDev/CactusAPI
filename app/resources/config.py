"""Config resource"""

from flask import request

from flask_restplus import Resource, marshal

from ..models import Config
from ..schemas import ConfigSchema
from ..util import helpers

# TODO: Solve createdAt cannot be formatted as datetime bug


class ConfigResource(Resource):

    def get(self, **kwargs):
        attributes, errors, code = helpers.single_response(
            "config", Config, token=kwargs["token"].lower()
        )

        response = {}

        if errors != []:
            response["errors"] = errors
        else:
            response["data"] = attributes

        return response, code

    def patch(self, **kwargs):
        json_data = request.get_json()

        if json_data is None:
            return {"errors": ["Bro...no data"]}, 400

        data = {**json_data, "token": kwargs["token"].lower()}

        # TODO: Need to add ability to just edit because EXPLOSIONS probs
        # for sure gonna happen
        attributes, errors, code = helpers.create_or_update(
            "config", Config, data, ["token", *json_data.keys()]
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
