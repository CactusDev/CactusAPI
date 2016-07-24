"""Run the API."""

from flask import Flask
import requests

APP = Flask(__name__)
APP.config.from_pyfile("config.py", True)

from views import *


def make_request(endpoint, request_type, params):
    """Make a request."""

    if request_type.lower() == "get":
        return requests.get(endpoint, params=params).json()
    elif request_type.lower() == "post":
        return requests.post(endpoint, data=params).json()


if __name__ == "__main__":
    APP.run(port=8000, host="0.0.0.0", debug=True)
