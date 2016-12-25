"""Config."""

RDB_DB = "api"
RDB_HOST = "localhost"
RDB_PORT = 28015

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
