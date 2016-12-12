from datetime import datetime
from ..schemas import SocialSchema


class Social:

    schema = SocialSchema()

    def __init__(self, *, token, service, url, **kwargs):
        if "id" in kwargs:
            self.id = kwargs["id"]
        self.token = token.lower()
        self.service = service
        self.url = url
