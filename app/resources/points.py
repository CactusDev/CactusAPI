"""Allows lookup and changing of points"""

from flask_restplus import Resource

from .. import api
from ..models import Point
from ..schemas import PointSchema
from ..util import helpers, auth
from ..util.helpers import APIError
from .. import limiter


class PointResource(Resource):
    """
    Allows lookup and editing of points by user ID
    """

    @limiter.limit("1000/day;90/hour;20/minute")
    @helpers.lower_kwargs("token")
    def get(self, path_data, **kwargs):
        """
        Handles retrieval of points in a channel by channel token and username
        """
        data = {**kwargs, **path_data}
        attributes, errors, code = helpers.single_response(
            "points", Point, **data
        )

        response = {}

        if errors != []:
            response["errors"] = errors
        else:
            response["data"] = attributes

        return response, code

    @limiter.limit("1000/day;90/hour;20/minute")
    @auth.scopes_required({"point:manage"})
    @helpers.lower_kwargs("token")
    def patch(self, path_data, **kwargs):
        """
        Handles managing of points (addition/subtraction/transfer)
        """
        data = {**helpers.get_mixed_args(), **kwargs, **path_data}

        attributes, errors, code = helpers.single_response(
            "points", Point,
            **{"token": kwargs["token"].lower(), "username": kwargs["name"]}
        )

        if code == 200:
            new_count = data["count"]

            if not isinstance(new_count, str):
                raise APIError({"count": "Must be a string"}, code=400)

            count = attributes["attributes"]["count"]
            if new_count[0] == '+' and new_count[1:].isdigit():
                count = count + int(new_count[1:])
            elif new_count[0] == '-' and new_count[1:].isdigit():
                count = count - int(new_count[1:])

            response = helpers.update_record(
                "points", {"id": attributes["id"], "count": count})

            if response is not None:
                attributes = response

        response = {}

        if errors != []:
            response["errors"] = errors
        else:
            response["data"] = attributes

        return response, code
