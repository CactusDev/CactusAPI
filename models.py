"""
RethinkDB models for remodel
"""

from remodel.models import Model


class User(Model):
    """
    A remodel table model
    """
    has_many = ("Tickets", "TicketResponse")

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
    pass


class Roles(Model):
    """
    A remodel table model
    """
    pass


class Channels(Model):
    """
    A remodel table model
    """

    has_many = ("Messages", "Friend")

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Configuration(Model):
    """
    A remodel table model
    """
    pass


class Commands(Model):
    """
    A remodel table model
    """
    pass


class Messages(Model):
    """
    A remodel table model
    """
    pass


class Executions(Model):
    """
    A remodel table model
    """
    pass


class Quotes(Model):
    """
    A remodel table model
    """
    pass


class UserRole(Model):
    """
    A remodel table model
    """
    pass


class Tickets(Model):
    """
    A remodel table model
    """
    belongs_to = ('User',)


class TicketResponse(Model):
    """
    A remodel table model
    """
    belongs_to = ('User',)
