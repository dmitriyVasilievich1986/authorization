#!/usr/bin/env python
from django.core.management import execute_from_command_line
from django.db.transaction import get_connection
from psycopg2 import OperationalError
from os import environ
from time import sleep
import logging


def runserver(host: str, port: str, *args: tuple, **kwargs: dict) -> None:
    # make migrations and migrate
    execute_from_command_line([__name__, "makemigrations"])
    execute_from_command_line([__name__, "migrate"])

    # start server
    execute_from_command_line([__name__, "runserver", f"{host}:{port}"])


def data_base_check_connection(*args: tuple, **kwargs: dict) -> bool:
    MAX_DB_CONNECTION_TRY: int = 3
    connection = get_connection()
    db_text: str = "Host: {}, Port: {}".format(
        connection.settings_dict.get("HOST"),
        connection.settings_dict.get("PORT"),
    )
    while MAX_DB_CONNECTION_TRY:
        try:
            connection.connect()
            logging.debug(f"Connection succeded. {db_text}")
            return True
        except OperationalError:
            logging.warning(
                f'Fail to connect to db. Attempts left: {MAX_DB_CONNECTION_TRY}')
        MAX_DB_CONNECTION_TRY = MAX_DB_CONNECTION_TRY - 1
        sleep(3)
    logging.error(f'Fail to connect to db. {db_text}')
    return False


if __name__ == "__main__":
    HOST: str = environ.get("HOST", "0.0.0.0")
    PORT: str = environ.get("PORT", "3000")

    environ.setdefault('DJANGO_SETTINGS_MODULE', 'authorization.settings')
    if data_base_check_connection():
        runserver(host=HOST, port=PORT)
