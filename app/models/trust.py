from datetime import datetime
from ..schemas import TrustSchema


class Trust:

    schema = TrustSchema()

    def __init__(self, *, token, userName, userId, active=True, **kwargs):
        if "id" in kwargs:
            self.id = kwargs["id"]
        self.token = token.lower()
        self.userName = userName
        self.userId = userId
        self.active = active
