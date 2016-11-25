from datetime import datetime
from ..schemas import RepeatSchema


class Repeat:

    schema = RepeatSchema()

    def __init__(self, *, text, token, repeatId, duration=900, **kwargs):
        if "id" in kwargs:
            self.id = kwargs["id"]
        self.text = text
        self.duration = duration    # In seconds
        self.token = token
        self.repeatId = repeatId
