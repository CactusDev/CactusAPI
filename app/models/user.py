from remodel.models import Model

from ..schemas import UserSchema


class User(Model):

    schema = UserSchema()

    def __init__(self, *, token, **kwargs):
        if "id" in kwargs:
            self.id = kwargs["id"]
        if "newCommandId" in kwargs:
            self.newCommandId = kwargs["newCommandId"]

        self.token = token
