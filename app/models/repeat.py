from datetime import datetime
from ..schemas import RepeatSchema


class Repeat:

    schema = RepeatSchema()

    def __init__(self, *, token, commandName, repeatId, arguments,
                 period=900, **kwargs):
        if "id" in kwargs:
            self.id = kwargs["id"]
        self.period = period    # In seconds
        self.token = token
        self.commandName = commandName
        self.repeatId = repeatId
        self.arguments = arguments
