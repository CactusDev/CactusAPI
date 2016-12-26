import sys
import pytest
import rethinkdb as rethink

# Why this works, I don't know. Blech.
sys.path.append(".")


@pytest.fixture
def app(request):
    from app import app
    app.config["TESTING"] = True
    app.config["RDB_DB"] = "testing"
    r = rethink.connect(db="testing")

    def tearDown():
        for table in rethink.db("testing").table_list().run(r):
            rethink.db("testing").table(table).delete().run(r)

    request.addfinalizer(tearDown)

    return app
