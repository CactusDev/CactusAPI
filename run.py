"""Run the API."""

from flask import Flask
import requests

app = Flask(__name__)
app.config.from_pyfile("config.py", True)

from views import *

if __name__ == "__main__":
    app.run(port=8000, host="0.0.0.0", debug=True)
