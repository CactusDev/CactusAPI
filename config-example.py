"""Config."""

RDB_DB = "api"
RDB_HOST = "localhost"
RDB_PORT = 28015
RDB_USERNAME = "cactus"
RDB_PASSWORD = "superawesomepassword01!"

SECRET_KEY = "RANDOM SECRET KEY HERE"

DEBUG = True
PORT = 8000
HOST = "127.0.0.1"

OAUTH_CREDENTIALS = {
    "service_name": {
        "CLIENT_ID": "service ID",
        "CLIENT_SECRET": "service secret"
    }
}

API_PREFIX = "/api/v1"

CB_USERNAME = "CactusBotDev"
CB_PASSWORD = "SPAMEGGSFOOBAR"

AUTH_EXPIRATION = {
    "days": 0,
    "hours": 0,
    "minutes": 0,
    "seconds": 4
}

API_SCOPES = {
    "points:manage": 14,    # "000000000000001"
    "alias:create": 13,     # "000000000000010"
    "alias:manage": 12,     # "000000000000100"
    "command:create": 11,   # "000000000001000"
    "command:manage": 10,   # "000000000010000"
    "config:create": 9,     # "000000000100000"
    "config:manage": 8,     # "000000001000000"
    "quote:create": 7,      # "000000010000000"
    "quote:manage": 6,      # "000000100000000"
    "repeat:create": 5,     # "000001000000000"
    "repeat:manage": 4,     # "000010000000000"
    "social:create": 3,     # "000100000000000"
    "social:manage": 2,     # "001000000000000"
    "trust:create": 1,      # "010000000000000"
    "trust:manage": 0,      # "100000000000000"
}

SENTRY_DSN = "https://supersecretsentryDSN.net"
# Tells the API whether or not to activate Sentry, disabled by default
SENTRY_ACTIVE = False
