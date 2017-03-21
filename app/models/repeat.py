from datetime import datetime
from ..schemas import RepeatSchema


class Repeat:

    schema = RepeatSchema()

    def __init__(self, *, token, commandName, repeatName, command, createdAt,
                 period=900, **kwargs):
        if "id" in kwargs:
            self.id = kwargs["id"]
        self.period = period    # In seconds
        self.token = token
        self.commandName = commandName
        self.command = command
        self.repeatName = repeatName
        self.createdAt = createdAt
