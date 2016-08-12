"""
RethinkDB models for remodel
"""

from remodel.models import Model


class User(Model):
    """
    A remodel table model
    """
    has_many = ("Ticket", "TicketResponse")
    has_one = ("Channel", )

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


class Role(Model):
    """
    A remodel table model
    """
    pass


class Channel(Model):
    """
    A remodel table model
    """

    has_many = ("Message", "Friend", "Message")
    has_one = ("User", )

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Configuration(Model):
    """
    A remodel table model
    """
    pass


class Command(Model):
    """
    A remodel table model
    """
    pass


class Message(Model):
    """
    A remodel table model
    """
    belongs_to = ("Channel", )


class Execution(Model):
    """
    A remodel table model
    """
    pass


class Quote(Model):
    """
    A remodel table model
    """
    pass


class UserRole(Model):
    """
    A remodel table model
    """
    pass


class Ticket(Model):
    """
    A remodel table model
    """
    belongs_to = ('User',)


class TicketResponse(Model):
    """
    A remodel table model
    """
    belongs_to = ('User',)
