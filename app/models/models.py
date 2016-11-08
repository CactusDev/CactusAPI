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
