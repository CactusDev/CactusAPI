from datetime import datetime
from ..schemas import CmdAliasSchema


class Alias:

    schema = CmdAliasSchema()

    def __init__(self, *, name, token, arguments, commandName="",
                 createdAt, enabled=True, **kwargs):
        if "id" in kwargs:
            self.id = kwargs["id"]
        self.name = name
        self.token = token
        self.createdAt = createdAt
        self.commandName = commandName
        self.enabled = enabled
        self.arguments = arguments
