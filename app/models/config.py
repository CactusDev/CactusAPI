from ..schemas import ConfigSchema


class Config:
    schema = ConfigSchema()

    def __init__(self, token=None, services=None, announce=None, spam=None,
                 **kwargs):
        # TODO: Don't add if None
        self.token = token
        self.services = services
        self.announce = announce
        self.spam = spam
