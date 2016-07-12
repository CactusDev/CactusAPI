"""Run the API."""

from flask import Flask
import requests

APP = Flask(__name__)
APP.config.from_pyfile("config.py", True)

from views import *


def make_request(endpoint, params, request_type):
    """Make a request."""

    if request_type == "get":
        return requests.get(api_base + endpoint, params=params)
    elif request_type == "post":
        return requests.post(api_base + endpoint, data=params)


if __name__ == "__main__":
    APP.run(port=8000, host="0.0.0.0", debug=True)
