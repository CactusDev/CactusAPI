"""Run the API."""

import argparse
import logging
import coloredlogs
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

        import rethinkdb as rethink
        from rethinkdb.errors import ReqlDriverError
        from app import models

        changes_made = False

        try:
            conn = rethink.connect(RDB_HOST, RDB_PORT)
        except ReqlDriverError as error:
            logging.error("Failed to connect to database at '{}:{}'!".format(
                RDB_HOST, RDB_PORT))
            logging.fatal(error)
            raise SystemExit

        if not rethink.db_list().contains(RDB_DB).run(conn):
            rethink.db_create(RDB_DB).run(conn)
            logging.info("Database '{}' successfully created!".format(RDB_DB))
            changes_made = True

        for db in models.tables:
            if not rethink.db(RDB_DB).table_list().contains(db).run(conn):
                rethink.db(RDB_DB).table_create(db).run(conn)
                logging.info("Table '{}' successfully created in DB "
                             "'{}'".format(
                                 db, RDB_DB
                             ))
                changes_made = True

        if changes_made:
            logging.warn("Database and tables successfully created!")
        else:
            logging.warn("No changes made!")

        raise SystemExit

    logging.debug(app.url_map)

    debug_mode = False
    if args.debug == "DEBUG":
        debug_mode = True

    app.run(
        port=app.config.get("PORT", 80),
        host=app.config.get("HOST", "0.0.0.0"),
        debug=debug_mode)
