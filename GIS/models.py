from django.contrib.gis.db import models

class GeoData(models.Model):
    geometry_collection = models.GeometryCollectionField()
