from datetime import datetime
from ..schemas import CmdAliasSchema


class Alias:

    schema = CmdAliasSchema()

    def __init__(self, *, aliasName, token, command="",
                 createdAt=datetime.utcnow(), enabled=True, **kwargs):
        if "id" in kwargs:
            self.id = kwargs["id"]
        self.aliasName = aliasName
        self.token = token
        self.createdAt = createdAt
        self.command = command
        self.enabled = enabled
