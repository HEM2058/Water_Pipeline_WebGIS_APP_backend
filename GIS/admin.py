from django.contrib import admin
from .models import GeoData, GeoJSONFile
from django.contrib.gis.admin import OSMGeoAdmin
# Register your models here.

admin.site.register(GeoData, OSMGeoAdmin)
admin.site.register(GeoJSONFile)