"""Allows lookup and changing of points"""

from flask_restplus import Resource

from .. import api
from ..models import Points
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
        data = {"username": kwargs["name"], **path_data}
        attributes, errors, code = helpers.single_response(
            "points", Points, **data
        )

        response = {}

        if errors != {}:
            response["errors"] = errors
        else:
            response["data"] = attributes

        return response, code

    @limiter.limit("1000/day;90/hour;20/minute")
    @auth.scopes_required({"points:manage"})
    @helpers.lower_kwargs("token")
    def patch(self, path_data, **kwargs):
        """
        Handles managing of points (addition/subtraction/transfer)
        """
        data = {**helpers.get_mixed_args(), **kwargs, **path_data}

        attributes, errors, code = helpers.single_response(
            "points", Points,
            **{"token": kwargs["token"].lower(), "username": kwargs["name"]}
        )

        if errors != {}:
            raise APIError(errors, code=code)

        if not isinstance(data["count"], str):
            raise APIError({"count": "Must be a string"}, code=400)

        try:
            if not data["count"][1:].isdigit():
                raise APIError(
                    {"count": "Non-integer value after first character"},
                    code=400)
            if data["count"][0] == '+':
                new_count = int(data["count"][1:])
            elif data["count"][0] == '-':
                new_count = int(data["count"][1:]) * -1
        except ValueError as err:
            errors = {
                "count": err.args()
            }

        if code == 200:
            count = attributes["attributes"]["count"] + new_count
        elif code == 404:
            # User doesn't have any points yet
            count = new_count

        if count < 0:
            # Not enough points to remove requested amount
            errors = [
                "{} missing {} points".format(
                    kwargs["name"], str(count)[1:]),
            ]

        attributes, errors, code = helpers.create_or_update(
            "points", Points,
            {**path_data, "username": kwargs["name"], "count": count}
        )

        response = {}

        if errors != {}:
            response["errors"] = errors
        else:
            response["data"] = attributes

        return response, code
