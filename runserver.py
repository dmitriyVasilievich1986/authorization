#!/usr/bin/env python
from django.core.management import execute_from_command_line
from dotenv import load_dotenv
from os import environ


def runserver(host, port, *args, **kwargs):
    # make migrations and migrate
    execute_from_command_line([__name__, "makemigrations"])
    execute_from_command_line([__name__, "migrate"])

    # start server
    execute_from_command_line([__name__, "runserver", f"{host}:{port}"])


if __name__ == "__main__":
    load_dotenv()

    HOST: str = environ.get("HOST", "0.0.0.0")
    PORT: str = environ.get("PORT", "3000")

    environ.setdefault('DJANGO_SETTINGS_MODULE', 'authorization.settings')
    runserver(host=HOST, port=PORT)
