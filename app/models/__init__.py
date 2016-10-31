from datetime import datetime

from .command import Command

fields_map = {
    "string": str,
    "integer": int,
    "boolean": bool,
    "datetime": datetime
}

__all__ = ["Command"]
