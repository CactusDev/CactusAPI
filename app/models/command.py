from datetime import datetime
from ..schemas import CommandSchema


class Command:

    schema = CommandSchema()

    def __init__(self, *, name, response, token, userLevel=0, **kwargs):
        if "id" in kwargs:
            self.id = kwargs["id"]
        self.name = name
        self.response = response
        self.token = token.lower()
        self.createdAt = datetime.utcnow()
        self.enabled = True
        self.deleted = False
        self.userLevel = userLevel
