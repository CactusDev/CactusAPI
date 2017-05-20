from datetime import datetime
from ..schemas import CommandSchema


class Command:

    schema = CommandSchema()

    force_on_create = {"response": "message"}

    def __init__(self, *, name, response, token, role=0,
                 createdAt, deletedAt, enabled=True,
                 arguments, count, **kwargs):
        if "id" in kwargs:
            self.id = kwargs["id"]
        self.name = name
        self.response = response
        self.token = token.lower()
        self.createdAt = createdAt
        self.enabled = enabled
        self.role = role
        self.arguments = arguments
        self.count = count
        self.deletedAt = deletedAt
