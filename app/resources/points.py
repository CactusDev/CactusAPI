"""Allows lookup and changing of points"""

from flask_restplus import Resource

from .. import api
from ..models import Points, PointCreationModel
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

        sender = data.get("sender")
        points = data.get("count")
        errors = {}

        validated = helpers.validate_data(
            PointCreationModel, helpers.get_mixed_args())
        if validated is not None:
            raise APIError(validated, code=500)

        # # Check if sendee has points yet
        # exists_or_error, code = helpers.resource_exists(
        #     "points", **path_data, username=kwargs["name"])
        # if code == 404:
        #     # Sendee does not exist
        #     pass
        #
        # print(exists_or_error, code)

        # Retrieve sender's points
        attributes, errors, code = helpers.single_response(
            "points", Points, username=sender, **path_data)

        print(attributes, code)
        print(errors)

        # Sender has enough points?
        # Remove # from sender
        # Check if error
        # Add # to sendee
        # Check if error
        # If either errored then roll back changes
        # Respond with changes or errors

        # try:
        #     if not data["count"][1:].isdigit():
        #         raise APIError(
        #             {"count": "Non-integer value after first character"},
        #             code=400)
        #     if data["count"][0] == '+':
        #         new_count = int(data["count"][1:])
        #     elif data["count"][0] == '-':
        #         new_count = int(data["count"][1:]) * -1
        # except ValueError as err:
        #     errors = {
        #         "count": err.args()
        #     }
        #
        # sender_count = attributes["attributes"]["count"]
        # if code == 200:
        #     count = sender_count + new_count
        # elif code == 404:
        #     # User doesn't have any points yet
        #     count = new_count
        #
        # if count < 0:
        #     # Not enough points to remove requested amount
        #     raise APIError("{name} missing {val} points".format(
        #         name=kwargs["name"], val=str(count)[1:]))
        #
        # # Update both records (sendee/sender)
        # # Add points to sendee
        # attributes, errors, code = helpers.create_or_update(
        #     "points", Points,
        #     {**path_data, "username": kwargs["name"], "count": count},
        #     **{**path_data, "username": kwargs["name"]}
        # )
        # # Remove points from sender
        # attributes, errors, code = helpers.update_resource(
        #     "points", Points,
        #     {"count": attributes["attributes"]["count"]}
        # )
        # Check that neither failed
        # If one failed we should roll back the changes
        response = {}

        if errors != {}:
            response["errors"] = errors
        else:
            response["data"] = attributes

        return response, code
