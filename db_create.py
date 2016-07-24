"""
Initializes the RethinkDB with the tables we need
Simply add a new class as needed to create new tables

The MIT License (MIT)

Copyright (c) RPiAwesomeness 2016

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import remodel.helpers
import remodel.connection
import rethinkdb as rethink
from rethinkdb.errors import ReqlDriverError
from models import *
from config import *

try:
    conn = rethink.connect(RDB_HOST, RDB_PORT)
except ReqlDriverError as error:
    print("Failed to connect to database at '{}:{}'!".format(
        RDB_HOST, RDB_PORT))
    print(error)
    raise SystemExit

if not rethink.db_list().contains(RDB_DB).run(conn):
    rethink.db_create(RDB_DB).run(conn)
    print("Database {} successfully created!".format(RDB_DB))

remodel.connection.pool.configure(db=RDB_DB)

remodel.helpers.create_tables()
remodel.helpers.create_indexes()
