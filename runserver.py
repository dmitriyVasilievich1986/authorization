#!/usr/bin/env python
from django.core.management import execute_from_command_line
from os import environ

HOST: str = environ.get("HOST", "0.0.0.0")
PORT: str = environ.get("PORT", "3000")

environ.setdefault('DJANGO_SETTINGS_MODULE', 'authorization.settings')
execute_from_command_line([__name__, "runserver", f"{HOST}:{PORT}"])
