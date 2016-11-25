from datetime import datetime
from ..schemas import RepeatSchema


class Repeat:

    schema = RepeatSchema()

    def __init__(self, *, text, token, repeatId, period=900, **kwargs):
        if "id" in kwargs:
            self.id = kwargs["id"]
        self.text = text
        self.period = period    # In seconds
        self.token = token
        self.repeatId = repeatId
