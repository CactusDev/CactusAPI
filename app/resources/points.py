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
        data = {**kwargs, **path_data}
