from ..schemas import UserSchema


class User:

    schema = UserSchema()

    ignore = ("password", )
    force_on_create = {"token"}

    def __init__(self, *, token, userName, userId, service="beam",
                 password=None, **kwargs):
        if "id" in kwargs:
            self.id = kwargs["id"]

        self.token = token.lower()  # token used to link data across tables
        self.userName = userName    # user name on service
        self.service = service      # Default (acct. creation) service
        self.userId = userId        # user ID on default service
        self.password = password    # API access password
