from datetime import datetime
from ..schemas import CommandSchema


class Command:

    schema = CommandSchema()

    def __init__(self, *, name, response, token, userLevel=0,
                 createdAt=datetime.utcnow(), enabled=True, **kwargs):
        if "id" in kwargs:
            self.id = kwargs["id"]
        self.name = name
        self.response = response
        self.token = token.lower()
        self.createdAt = createdAt
        self.enabled = enabled
        self.userLevel = userLevel
