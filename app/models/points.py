from datetime import datetime
from ..schemas import PointsSchema


class Points:
    schema = PointsSchema()

    def __init__(self, *, count, createdAt, token, username, **kwargs):
        if "id" in kwargs:
            self.id = kwargs["id"]
        self.username = username
        self.count = count
        self.createdAt = createdAt
        self.token = token
