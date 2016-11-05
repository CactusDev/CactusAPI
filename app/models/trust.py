from datetime import datetime

from remodel.models import Model

from ..schemas import TrustSchema


class Trust(Model):

    schema = TrustSchema()

    def __init__(self, *, token, userName, userId, active=True, **kwargs):
        if "id" in kwargs:
            self.id = kwargs["id"]
        self.token = token
        self.userName = userName
        self.userId = userId
        self.active = active
