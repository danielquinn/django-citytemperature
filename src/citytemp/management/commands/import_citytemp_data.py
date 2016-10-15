import lzma
import os

from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    """
    This package comes with *a lot* of data, so much that we can't distribute
    it in Django's preferred .json fixutres format as it has been known to
    explode some systems in the past.  Instead, we have to pull them in as raw
    SQL.

    Additionally, one of those .sql files is compressed user LZMA, so we have
    to decompress it before dumping it to the db.

    So why didn't we do this as a migration?  Well originally, that was the
    case, but it turns out that that effectively cripples the test framework as
    the migrations run for every test run.
    """

    help = "Imports all of the data in the citytemp app into the database."

    def handle(self, *args, **options):
        cursor = connection.cursor()

        sql = os.path.normpath(os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "..", "..", "sql"))

        with open(os.path.join(sql, "city.sql")) as f:
            cursor.execute(f.read())

        with lzma.open(os.path.join(sql, "temperature.sql.xz")) as f:
            cursor.execute(f.read())
