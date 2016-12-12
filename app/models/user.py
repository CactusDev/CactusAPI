from ..schemas import UserSchema


class User:

    schema = UserSchema()

    def __init__(self, *, token, userName, userId, service="beam", **kwargs):
        if "id" in kwargs:
            self.id = kwargs["id"]

        self.token = token.lower()  # token used to link data across tables
        self.userName = userName    # user name on service
        self.service = service      # Default (acct. creation) service
        self.userId = userId        # user ID on default service
