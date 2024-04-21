"""
Django command to wait for the database to be available
"""

import time

from psycopg2 import OperationalError as Psycopg2Error

from django.db.utils import (
    OperationalError,
)  # Error Django throws when database is not ready

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to wait for database."""

    def handle(self, *args, **options):
        """Entrypoint for command."""

        # stdout is just the standard output that we can use to log things to the screen as our command and executing
        self.stdout.write("Waiting for database...")
        db_up = False

        while db_up is False:
            try:
                self.check(databases=["default"])
                db_up = True
            except (Psycopg2Error, OperationalError):
                self.stdout.write("Database unavailable! Waiting for 1 second....")
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS("Database available!"))
