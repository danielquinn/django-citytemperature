# django-citytemperature

This database took a Very Long Time to compile, so I thought that I'd share
it.

**django-citytemp** is a collection of major cities around the world along
with their coordinates in PostGIS format, timezone, elevation and
temperature highs, lows, mean, and records data conveniently packaged into a
Django app.

If you're not using Django, the data should still be accessible.  Everything
you need is in the `sql/` directory.  `_structure.sql` has the table
definitions, `city.sql` is the basic city information and `temperature.sql.xz`
is an LZW-compressed SQL file containing all of the temperature data.


## Requirements

If you're using Django, you'll need to install`django-countries` to make use
of the country data in the city table.

If however you're not using django, then the data alone requires nothing.


## Installation

For Django users, the data should install automatically when you run
`manage.py migrate`.  Note that it may take a while though, since the
temperature data is just over 350k records.  Low-memory systems may balk at
the way the import is done (one shot, all the data), so you may need to edit
the file if your memory requirements are too low.


## How to use it

The easiest way to get a city from the database is to query by airport code:

```python
from citytemp.models import City

amsterdam = City.objects.get(code="AMS")
```

But since we've got geographic data in there, we can also do fun things like
get the *nearest* city to an arbitrary point:

```python
from citytemp.models import City
from django.contrib.gis.geos import *
from django.contrib.gis.measure import D

centre = fromstr("POINT({lng} {lat})".format(lat=lat, lng=lng))
nearest_city = City.objects.filter(
    location__distance_lte=(centre, D(km=1000))
).distance(
    centre
).order_by(
    "distance"
).first()
```

Whatever method you use to get the city, you can then use the data we've
collected for it:

```python
print(amsterdam.code)
print(amsterdam.timezone)
print(amsterdam.elevation)
print(amsterdam.location.get_coords())

# If you have arrow, you can get the current time in a city:
print(arrow.now(amsterdam.timezone))

now = datetime.now()
for temperature in amsterdam.temperatures.filter(month=now.month, day=now.day):
    print(temperature.mean, temperature.record_high, temperature.daily_low)
```

It should be noted that this is by no means a complete database.  I've
collected all of this from snippets of databases all over the place, but I've
found it to be complete *enough* for my purposes.  Maybe you will too.


## To Do:

The models themselves are rather simple, lacking even basic helper methods to
make use of the data.

