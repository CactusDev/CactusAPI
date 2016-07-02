from flask import Flask, jsonify
from datetime import datetime
import requests

app = Flask(__name__)
app.config.from_pyfile("config.py", True)

from views import *


def make_request(endpoint, params, type):
    if type == "get":
        return requests.get(api_base + endpoint, params=params)
    elif type == "post":
        return requests.post(api_base + endpoint, data=params)


if __name__ == "__main__":
    app.run(port=8000, host="0.0.0.0", debug=True)
