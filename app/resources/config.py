"""Config resource"""

from flask import request

from flask_restplus import Resource, marshal

from ..models import Config
from ..schemas import ConfigSchema
from ..util import helpers, auth
from .. import limiter


class ConfigResource(Resource):

    @limiter.limit("1000/day;90/hour;20/minute")
    @helpers.lower_kwargs("token")
    def get(self, path_data, **kwargs):
        attributes, errors, code = helpers.single_response(
            "config", Config, **path_data)

        response = {}

        if errors != {}:
            response["errors"] = errors
        else:
            to_return = {}
            # WARNING - CONFUSIFICATING/UGLY CODE AHEAD. PROCEED WITH CAUTION
            # TODO: Clean this crap up
            # Only return the config options they want
            data = helpers.get_mixed_args()

            if data == {}:
                response["data"] = attributes

                return response, code

            for key in data.get("keys", []):
                if ':' in key:
                    # Split the key, only take the first two results
                    primary_key, sub_key = key.split(':')[:2]
                    if primary_key not in to_return:
                        to_return[primary_key] = {}

                    attr = attributes["attributes"]

                    if primary_key in attr:
                        if isinstance(attr[primary_key], list):
                            if sub_key.isdigit():
                                if len(attr[primary_key]) - 1 >= int(sub_key):
                                    to_return[primary_key][sub_key] = attr[
                                        primary_key][int(sub_key)]

                        if sub_key in attr[primary_key]:
                            to_return[primary_key][sub_key] = attr[
                                primary_key][sub_key]
                    else:
                        to_return[primary_key][sub_key] = "Config not found"
                else:
                    if key not in attributes["attributes"]:
                        to_return[key] = "Config not found"
                        continue

                    to_return[key] = attributes["attributes"][key]

            response["data"] = to_return

        return response, code

    @limiter.limit("1000/day;90/hour;20/minute")
    @auth.scopes_required({"config:manage"})
    @helpers.lower_kwargs("token")
    def patch(self, path_data, **kwargs):
        data = {**helpers.get_mixed_args(), **path_data}

        attributes, errors, code = helpers.create_or_update(
            "config", Config, data, **path_data
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
