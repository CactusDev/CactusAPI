from datetime import datetime
from ..schemas import CommandSchema


class Command:

    schema = CommandSchema()

    force_on_create = {"response": "message"}

    def __init__(self, *, name, response, token, userLevel=0,
                 createdAt=datetime.utcnow(), enabled=True,
                 arguments, count, **kwargs):
        if "id" in kwargs:
            self.id = kwargs["id"]
        self.name = name
        self.response = response
        self.token = token.lower()
        self.createdAt = createdAt
        self.enabled = enabled
        self.userLevel = userLevel
        self.arguments = arguments
        self.count = count
