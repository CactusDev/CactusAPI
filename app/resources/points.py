"""Allows lookup and changing of points"""

from flask_restplus import Resource

from .. import api
from ..models import Points, PointCreationModel
from ..schemas import PointSchema
from ..util import helpers, auth
from ..util.helpers import APIError, InternalServerError
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
        # TODO: Clean up this endpoint
        data = {**helpers.get_mixed_args(), **kwargs, **path_data}

        sender = data.get("sender")
        sendee = kwargs["name"]
        count = data.get("count")
        errors = {}

        validated = helpers.validate_data(
            PointCreationModel, helpers.get_mixed_args())
        if validated is not None:
            raise APIError(validated, code=500)

        # Retrieve sender's points
        attributes, errors, code = helpers.single_response(
            "points", Points, username=sender, **path_data)

        if code == 200:
            sender_points = attributes["attributes"]["count"]
        else:
            raise APIError({"sender": ["Missing required number of points"]},
                           code=400)

        try:
            if not data["count"][1:].isdigit():
                raise APIError(
                    {"count": "Non-integer value after first character"},
                    code=400)
        except ValueError as err:
            raise APIError({
                "count": err.args()
            })

        if sendee == "CactusBot":
            # This is an in-bot usage, don't give it to anyone
            pass

        # Sender has enough points?
        diff = sender_points - int(data["count"][1:])
        if diff < 0:
            raise APIError("{name} missing {val} points".format(
                name=sender, val=count[1:]), code=400)
        else:
            # Retrieve sendee's points
            attributes, errors, code = helpers.single_response(
                "points", Points, username=sendee, **path_data)

            sendee_points = 0
            if code == 200:
                # Sendee is in DB, use the points there
                sendee_points = attributes["attributes"]["count"]

            # TODO: Move this block into a helper function, atomic_changes()
            # Remove # from sender
            attributes, errors, code = helpers.update_resource(
                "points", Points, {"count": diff},
                **path_data, username=sender
            )
            # Check if error
            if code != 200:
                raise InternalServerError()

            # Add # to sendee
            attributes, errors, code = helpers.create_or_update(
                "points", Points,
                {
                    "count": sendee_points + int(data["count"][1:]),
                    "username": sendee,
                    **path_data
                },
                **path_data, username=sendee
            )
            # Check if error
            if code not in (200, 201):
                # Roll back sender's points
                attributes, errors, code = helpers.update_resource(
                    "points", Points, {"count": sender_points},
                    **path_data, username=sender
                )
                raise InternalServerError()

        response = {}

        if errors != {}:
            response["errors"] = errors
        else:
            response["data"] = attributes

        return response, code
