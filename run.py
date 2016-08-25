"""Run the API."""

from flask import Flask
import requests

APP = Flask(__name__)
APP.config.from_pyfile("config.py", True)

from views import *

if __name__ == "__main__":
    APP.run(port=8000, host="0.0.0.0", debug=True)
