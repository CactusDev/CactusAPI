from datetime import datetime
from ..schemas import CommandSchema


class Command:

    schema = CommandSchema()

    def __init__(self, *, name, response, token, createdAt=datetime.utcnow(),
                 userLevel=0, **kwargs):
        if "id" in kwargs:
            self.id = kwargs["id"]
        self.name = name
        self.response = response
        self.token = token.lower()
        self.createdAt = createdAt
        self.enabled = True
        self.deleted = False
        self.userLevel = userLevel
