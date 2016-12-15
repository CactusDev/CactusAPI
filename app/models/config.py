from .. import app
from ..schemas import ConfigSchema


class Config:
    schema = ConfigSchema()

    ignore = ("password", )

    def __init__(self, token=None, services=None, announce=None, spam=None,
                 **kwargs):
        # TODO: Don't add if None
        self.token = token
        self.services = services
        self.announce = announce
        self.spam = spam

    @staticmethod
    def default_data(token=None):
        return {
            "token": token.lower(),
            "services": [Service().__dict__],
            "announce": Announcements().__dict__,
            "spam": Spam().__dict__
        }


class Service:
    """
    Dummy class to keep track of sub-configs. Perhaps will implement proper
    loading later
    """

    def __init__(self,
                 name="beam",
                 isOAuth=False,
                 username=app.config.get("CB_USERNAME", "CactusBotDev"),
                 password=app.config.get("CB_PASSWORD", None),
                 permissions=["chat:connect", "chat:chat"]):
        self.name = name
        self.isOAuth = isOAuth
        self.username = username
        self.password = password
        self.permissions = permissions


class Announcements:
    """
    Dummy class to keep track of sub-configs. Perhaps will implement proper
    loading later
    """
    def default(announcement):
        return {
            "announce": False,
            "message": "Thanks for the {}, %NAME%!".format(announcement)
        }

    def __init__(self,
                 follow=default("follow"),
                 join=default("join"),
                 leave=default("leave"),
                 sub=default("subscription"),
                 host=default("host")):
        self.follow = follow
        self.join = join
        self.leave = leave
        self.sub = sub
        self.host = host


class Spam:
    """
    Dummy class to keep track of sub-configs. Perhaps will implement proper
    loading later
    """

    def __init__(self,
                 maxEmoji=12,
                 autoTimeout=False,
                 notifyMod={"notify": False, "userNames": []},
                 allowLinks=True):
        self.maxEmoji = maxEmoji
        self.autoTimeout = autoTimeout
        self.notifyMod = notifyMod
        self.allowLinks = allowLinks
