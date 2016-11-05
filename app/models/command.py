from datetime import datetime

from remodel.models import Model

from ..schemas import CommandSchema


class Command(Model):

    schema = CommandSchema()

    def __init__(self, *, name, response, commandId, token, userLevel=0,
                 **kwargs):
        if "id" in kwargs:
            self.id = kwargs["id"]
        self.name = name
        self.response = response
        self.commandId = commandId
        self.token = token
        self.createdAt = datetime.utcnow()
        self.enabled = True
        self.deleted = False
        self.userLevel = userLevel
