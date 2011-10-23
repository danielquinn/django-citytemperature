from django.contrib.gis.db import models

class City(models.Model):

    country   = models.CharField(max_length=32)
    city      = models.CharField(max_length=32)
    code      = models.CharField(max_length=4)
    location  = models.PointField(geography=True)
    elevation = models.IntegerField(blank=True, null=True)

    def __unicode__(self):
        return "%s, %s (%s)" % (self.city, self.country, self.code)



class Temperature(models.Model):

    MONTHS = (
        (1,"January"),
        (2,"February"),
        (3,"March"),
        (4,"April"),
        (5,"May"),
        (6,"June"),
        (7,"July"),
        (8,"August"),
        (9,"September"),
        (10,"October"),
        (11,"November"),
        (12,"December"),
    )

    airport = models.ForeignKey(City)
    month   = models.PositiveIntegerField(choices=MONTHS)
    day     = models.PositiveIntegerField(choices=((date,date) for date in range(1,32)))
    high    = models.IntegerField(blank=True,null=True)
    low     = models.IntegerField(blank=True,null=True)
    mean    = models.IntegerField(blank=True,null=True)
    rhigh   = models.IntegerField(blank=True,null=True)
    rlow    = models.IntegerField(blank=True,null=True)

