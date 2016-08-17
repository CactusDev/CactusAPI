"""
RethinkDB models for remodel
"""

from remodel.models import Model
from rethinkdb import now


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
          "type": type(now)
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


class Friend(Model):
    """
    A remodel table model
    """
    belongs_to = ('Channel', )
    has_one = ("User", )
    ignore = ["owner", "userId"]
    fields = {
        "channelId": {
            "type": int
        },
        "token": {
            "type": str
        },
        "userName": {
            "type": str
        },
        "userId": {
            "type": int
        },
        "active": {
            "type": bool,
            "default": True
        }
    }


class Role(Model):
    """
    A remodel table model
    """
    fields = {}
    ignore = []


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
    fields = {}


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


class Quote(Model):
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
