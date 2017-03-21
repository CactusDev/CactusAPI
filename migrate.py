import rethinkdb as rethink
from app import app
from app import schemas
from pprint import pprint
from marshmallow import fields


class RethinkConnnection:
    defaults = {
        fields.String: "",
        fields.Integer: 0,
        fields.Boolean: True,
        # fields.Nested: {}, # Going to be a paaaaain
        fields.List: []
    }

    def __init__(self, database=app.config["RDB_DB"],
                 host=app.config["RDB_HOST"],
                 port=app.config["RDB_PORT"],
                 blacklist=[]):
        self.db = database
        self.host = host
        self.port = port
        self.blacklist = blacklist
        self.connection = rethink.connect(
            host=self.host,
            db=self.db,
            port=self.port
        )

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            self.connection.close()
        except AttributeError:
            pass

    def get_tables(self):
        """Get the table list"""
        return list(rethink.table_list().run(self.connection))

    def get_values(self, table):
        """Get all the objects in the table"""
        return list(rethink.table(table).run(self.connection))

    def get_fields(self, table):
        """Returns a list of all the fields in the given table"""
        return set(rethink.table(table)
                   .map(lambda val: val.keys())
                   .reduce(lambda left, right: left + right)
                   .distinct()
                   .run(self.connection))

    def update_values(self, table, update_vals):
        """
        Take a table and a dictionary of new values to update with
        and update the table
        """
        pass

    def remove_fields(self, table, fields):
        """
        Take a table and a list of fields and remove those fields, then
        update the database
        """
        pass

if __name__ == "__main__":
    conn = RethinkConnnection()
    tables = [
        table for table in conn.get_tables()
        if table not in conn.blacklist
    ]
    table_fields = {
        table: conn.get_fields(table)
        for table in tables
    }

    for schema, table in schemas.table_map.items():
        print("table:\t", table)
        fields = set(getattr(schemas, schema)().fields.keys())
        missing_fields = [
            val for val in fields if val not in table_fields[table]
        ]
        print(missing_fields)
        for field in missing_fields:
            pprint(
                (getattr(schemas, schema)().fields)[field])
        print("------------------")

    # Backup DB
    # For each table:
    # Get record list
    # Compare all records' keys to current schemas
    # Remove fields removed in new schema
    # For each record in each table:
    # Insert new field. New value = annotation on field/else default for type
    # (0, "", true, etc.)
