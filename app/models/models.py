"""
RethinkDB models for remodel
"""

from remodel.models import Model
import rethinkdb as rethink
from datetime import datetime
import config


class User(Model):
    """
    A remodel table model
    """
    has_many = ("Ticket", "TicketResponse")
    has_one = ("Channel", )
    fields = {
        "active": {
            "type": bool,
            "default": True
        },
        "confirmed_at": {
            "type": datetime,
            "default": rethink.now().run(rethink.connect(
                db=config.RDB_DB,
                port=config.RDB_PORT,
                host=config.RDB_HOST
            ))
        },
        "email": {
            "type": str
        },
        "providerId": {
            "type": str
        },
        "roles": {
            "type": list
        },
        "userName": {
            "type": str
        }
    }

    def get_id(self):
        """
        Returns a string of the User object's ID
        """
        return str(self["id"])

    @property
    def is_active(self):
        """
        Returns a string of the User object's ID
        """
        return True

    @property
    def is_anonymous(self):
        """Check if the user is anonymous."""
        return True

    @property
    def is_authenticated(self):
        """Check if the user is authenticated."""
        return True


class Role(Model):
    """
    A remodel table model
    """
    fields = {}


class Channel(Model):
    """
    A remodel table model
    """

    has_many = ("Message", "Friend", "Message")
    has_one = ("User", )
    fields = {}

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Configuration(Model):
    """
    A remodel table model
    """
    fields = {}


class Command(Model):
    """
    A remodel table model
    """
    fields = {
        "name": {
            "type": str
        },
        "commandId": {
            "type": int
        },
        "response": {
            "type": str
        },
        "enabled": {
            "type": bool,
            "default": True,
        },
        "deleted": {
            "type": bool,
            "default": False
        },
        "userLevel": {
            "type": int,
            "default": 0
        },
        "createdAt": {
            "type": datetime,
            "default": rethink.now().run(rethink.connect(
                db=config.RDB_DB,
                port=config.RDB_PORT,
                host=config.RDB_HOST
            ))
        },
        "userId": {
            "type": str
        },
        "userName": {
            "type": str
        },
        "channelName": {
            "type": str
        },
        "channelId": {
            "type": str
        }
    }


class Message(Model):
    """
    A remodel table model
    """
    belongs_to = ("Channel", )
    fields = {}


class Execution(Model):
    """
    A remodel table model
    """
    fields = {}


class UserRole(Model):
    """
    A remodel table model
    """
    fields = {}


class Ticket(Model):
    """
    A remodel table model
    """
    belongs_to = ('User',)
    fields = {}


class TicketResponse(Model):
    """
    A remodel table model
    """
    belongs_to = ('User',)
    fields = {}
