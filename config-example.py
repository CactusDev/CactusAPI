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
        "CLIENT_ID": "service_ID",
        "CLIENT_SECRET": "service_secret"
    }
}

API_PREFIX = "/api/v1"
