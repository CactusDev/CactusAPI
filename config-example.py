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
    "alias:create": 13,     # "00000000000001",
    "alias:manage": 12,     # "00000000000010",
    "command:create": 11,   # "00000000000100",
    "command:manage": 10,   # "00000000001000",
    "config:create": 9,     # "00000000010000",
    "config:manage": 8,     # "00000000100000",
    "quote:create": 7,      # "00000001000000",
    "quote:manage": 6,      # "00000010000000",
    "repeat:create": 5,     # "00000100000000",
    "repeat:manage": 4,     # "00001000000000",
    "social:create": 3,     # "00010000000000",
    "social:manage": 2,     # "00100000000000",
    "trust:create": 1,      # "01000000000000",
    "trust:manage": 0,      # "10000000000000"
}

SENTRY_DSN = "https://supersecretsentryDSN.net"
SENTRY_ACTIVE = False  # Tells the API whether or not to activate Sentry, disabled by default
