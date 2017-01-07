import sys
import pytest
import rethinkdb as rethink
from os import environ

# Why this works, I don't know. Blech.
sys.path.append(".")


# def pytest_sessionstart(session):
#     if "APIKEY" not in environ:
#         pytest.exit("NEED THE API ACCESS KEY YA DANG FOOL")


def pytest_sessionfinish(session):
    r = rethink.connect(db="testing")
    for key in rethink.db("testing").table_list().run(r):
        rethink.db("testing").table(key).delete().run(r)


@pytest.fixture
def app(request):
    from app import app
    app.config["TESTING"] = True
    app.config["RDB_DB"] = "testing"
    # app.config["API_TOKEN"] = "root"
    # app.config["API_KEY"] = environ["APIKEY"]

    return app


@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client
