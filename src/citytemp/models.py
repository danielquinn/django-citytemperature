from django.contrib.gis.db import models

try:
    from django_countries.fields import CountryField
except ImportError:
    CountryField = models.CharField


class City(models.Model):

    country = CountryField(max_length=2)
    city = models.CharField(max_length=32)
    airport_code = models.CharField(max_length=4)
    location = models.PointField(geography=True)
    elevation = models.IntegerField(
        blank=True, null=True, help_text="In metres")
    timezone = models.CharField(max_length=64)

    objects = models.GeoManager()

    def __str__(self):
        return "{}, {} ({})".format(self.city, self.country, self.airport_code)



class Temperature(models.Model):

    MONTHS = (
        (1,  "January"),
        (2,  "February"),
        (3,  "March"),
        (4,  "April"),
        (5,  "May"),
        (6,  "June"),
        (7,  "July"),
        (8,  "August"),
        (9,  "September"),
        (10, "October"),
        (11, "November"),
        (12, "December"),
    )

    city = models.ForeignKey(City, related_name="temperatures")
    month = models.PositiveIntegerField(choices=MONTHS)
    day = models.PositiveIntegerField(
        choices=((date, date) for date in range(1, 32)))

    daily_high = models.IntegerField(
        blank=True, null=True, help_text="Daily high")
    daily_low = models.IntegerField(
        blank=True, null=True, help_text="Daily low")

    mean = models.IntegerField(
        blank=True, null=True, help_text="Mean temperature")

    record_high = models.IntegerField(
        blank=True, null=True, help_text="Record high")
    record_low = models.IntegerField(
        blank=True, null=True, help_text="Record low")

    def __str__(self):
        return "{}/{}: {}".format(self.month, self.day, self.mean)
