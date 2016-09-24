from __future__ import unicode_literals

import lzma
import os

import django.contrib.gis.db.models.fields
import django.db.models.deletion
import django_countries.fields

from django.db import connection, migrations, models


def populate_all_the_things(apps, schema_editor):
    """
    This package comes with *a lot* of data, so much that we can't distribute
    it in Django's preferred .json fixutres format as it has been known to
    explode some systems in the past.  Instead, we have to pull them in as raw
    SQL.

    Additionally, one of those .sql files is compressed user LZMA, so we have
    to decompress it before dumping it to the db.
    """

    cursor = connection.cursor()

    sql = os.path.normpath(os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "..", "sql"))

    with open(os.path.join(sql, "city.sql")) as f:
        cursor.execute(f.read())

    with lzma.open(os.path.join(sql, "temperature.sql.xz")) as f:
        cursor.execute(f.read())


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('city', models.CharField(max_length=32)),
                ('airport_code', models.CharField(max_length=4)),
                ('location', django.contrib.gis.db.models.fields.PointField(geography=True, srid=4326)),
                ('elevation', models.IntegerField(blank=True, help_text='In metres', null=True)),
                ('timezone', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Temperature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='temperatures', to='citytemp.City')),
                ('month', models.PositiveIntegerField(choices=[(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'), (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')])),
                ('day', models.PositiveIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24), (25, 25), (26, 26), (27, 27), (28, 28), (29, 29), (30, 30), (31, 31)])),
                ('daily_high', models.IntegerField(blank=True, help_text='Daily high', null=True)),
                ('daily_low', models.IntegerField(blank=True, help_text='Daily low', null=True)),
                ('mean', models.IntegerField(blank=True, help_text='Mean temperature', null=True)),
                ('record_high', models.IntegerField(blank=True, help_text='Record high', null=True)),
                ('record_low', models.IntegerField(blank=True, help_text='Record low', null=True)),
            ],
        ),
        migrations.RunPython(populate_all_the_things)
    ]
