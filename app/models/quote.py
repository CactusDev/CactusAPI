from datetime import datetime

from ..schemas import QuoteSchema


class Quote:
    schema = QuoteSchema()

    def __init__(self, *, quote, quoteId, token, createdAt, deletedAt,
                 enabled=True, **kwargs):
        if "id" in kwargs:
            self.id = kwargs["id"]
        self.quote = quote
        self.quoteId = quoteId
        self.token = token.lower()
        self.enabled = enabled
        self.createdAt = createdAt
        self.deletedAt = deletedAt
