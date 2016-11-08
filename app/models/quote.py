from datetime import datetime

from remodel.models import Model

from ..schemas import QuoteSchema


class Quote(Model):
    schema = QuoteSchema()

    def __init__(self, *, quote, quoteId, token, enabled=True, **kwargs):
        if "id" in kwargs:
            self.id = kwargs["id"]
        self.quote = quote
        self.quoteId = quoteId
        self.token = token
        self.enabled = enabled
        self.createdAt = datetime.utcnow()
