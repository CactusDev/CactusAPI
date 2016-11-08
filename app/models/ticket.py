from datetime import datetime

from remodel.models import Model

from ..schemas import TicketSchema


class Ticket(Model):
    schema = TicketSchema()

    def __init__(self, *, title, contents, flags, mentions, **kwargs):
        if "id" in kwargs:
            self.id = kwargs["id"]
        self.title = title
        self.contents = contents
        self.flags = flags
        self.createdAt = datetime.now()
        self.mentions = mentions
