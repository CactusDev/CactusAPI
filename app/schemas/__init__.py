from .command import CommandSchema
from .trust import TrustSchema
from .user import UserSchema
from .quote import QuoteSchema
from .repeats import RepeatSchema
from .alias import CmdAliasSchema
from .social import SocialSchema
from .config import ConfigSchema
from .points import PointSchema, PointCreationSchema

__all__ = ["CommandSchema", "TrustSchema", "SocialSchema", "ConfigSchema",
           "UserSchema", "QuoteSchema", "RepeatSchema", "CmdAliasSchema",
           "PointSchema", "PointCreationSchema"]

table_map = {
    "CommandSchema": "commands",
    "TrustSchema": "trusts",
    "ConfigSchema": "configs",
    "SocialSchema": "socials",
    "UserSchema": "users",
    "QuoteSchema": "quotes",
    "RepeatSchema": "repeats",
    "CmdAliasSchema": "aliases",
    "PointSchema": "points"
}
