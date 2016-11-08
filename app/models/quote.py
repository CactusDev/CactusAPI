from datetime import datetime

from ..schemas import QuoteSchema


class Quote:
    schema = QuoteSchema()

    def __init__(self, *, quote, quoteId, token, enabled=True, **kwargs):
        if "id" in kwargs:
            self.id = kwargs["id"]
        self.quote = quote
        self.quoteId = quoteId
        self.token = token
        self.enabled = enabled
        self.createdAt = datetime.utcnow()
