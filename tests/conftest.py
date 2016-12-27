import sys
import pytest
import rethinkdb as rethink

# Why this works, I don't know. Blech.
sys.path.append(".")


def pytest_sessionfinish(session):
    r = rethink.connect(db="testing")
    for key in rethink.db("testing").table_list().run(r):
        rethink.db("testing").table(key).delete().run(r)


@pytest.fixture
def app(request):
    from app import app
    app.config["TESTING"] = True
    app.config["RDB_DB"] = "testing"

    return app


@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client
