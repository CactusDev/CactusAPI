from datetime import datetime
from ..schemas import RepeatSchema


class Repeat:

    schema = RepeatSchema()

    def __init__(self, *, token, command="", repeatId, period=900,
                 **kwargs):
        if "id" in kwargs:
            self.id = kwargs["id"]
        self.period = period    # In seconds
        self.token = token
        self.command = command
        self.repeatId = repeatId
