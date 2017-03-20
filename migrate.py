import rethinkdb as rethink

# Backup DB


def test(foo: str) -> bool:
    return foo == "test"


def connect_to_rethink():
    # Connect to DB
    pass


class Foo:

    def __init__(self, foo: "explosions", bar):
        self.foo = foo
        self.bar = bar

    def __str__(self):
        return "<Foo {'foo': %s, 'bar': %s}>" % (self.foo, self.bar)

foo = Foo("foo", "spameggs")
print(foo)
# Get table list
# For each table:
# Get record list
# Compare all records' keys to current schemas
# Remove fields removed in new schema
# For each record in each table:
# Insert new field. New value = annotation on field/else default for type
# (0, "", true, etc.)
