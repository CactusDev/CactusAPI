"""Run the API."""

import argparse
import logging
import coloredlogs
from flask_restplus import Api
from app import app

parser = argparse.ArgumentParser()

parser.add_argument(
    "-c", "--create-db",
    default=False,
    action="store_true",
    help="Initialize the DB with the proper tables"
)

parser.add_argument(
    "--debug",
    help="Set custom logger level",
    metavar="LEVEL",
    nargs='?',
    const="DEBUG",
    default="INFO"
)

parser.add_argument

args = parser.parse_args()

logging.basicConfig(
    level=args.debug,
    format="{asctime} {levelname} {name} {funcName}: {message}",
    datefmt="%Y-%m-%d %H:%M:%S",
    style='{'
)

coloredlogs.install(level=args.debug)


if __name__ == "__main__":
    if args.create_db:
        RDB_HOST = app.config.get("RDB_HOST", None)
        RDB_DB = app.config.get("RDB_DB", None)
        RDB_PORT = app.config.get("RDB_PORT", None)

        if RDB_DB is None or RDB_HOST is None or RDB_PORT is None:
            logging.fatal("Config is not properly completed! Please copy",
                          "config-example.py to config.py and complete it!")
            raise SystemExit(-1)

        import remodel.helpers
        import remodel.connection
        import rethinkdb as rethink
        from rethinkdb.errors import ReqlDriverError
        from models import *

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

        remodel.connection.pool.configure(db=RDB_DB,
                                          host=RDB_HOST,
                                          port=RDB_PORT)

        remodel.helpers.create_tables()
        remodel.helpers.create_indexes()

        logging.info("Database and tables successfully created!")

        raise SystemExit

    print(app.url_map)

    app.run(
        port=app.config.get("PORT", 8000),
        host=app.config.get("HOST", "127.0.0.1"),
        debug=app.config.get("DEBUG", False))
