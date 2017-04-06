from .command import Command
from .trust import Trust
from .user import User
from .quote import Quote
from .repeat import Repeat
from .alias import Alias
from .social import Social
from .config import Config
from .points import Points

# Define the tables to create with the proper table name
tables = ["commands", "trusts", "users", "quotes", "repeats", "aliases",
          "socials", "configs", "builtins", "keys", "points"]


__all__ = ["Command", "Trust", "User", "Quote", "Repeat", "Alias", "Social",
           "Config", "Points"]
