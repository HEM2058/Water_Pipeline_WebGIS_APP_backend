from django.contrib import admin
from .models import Pipeline, PipelineFile, StorageUnit, StorageUnitFile, GateValve,  GateValveFile, TubeWell, TubeWellFile, Task, Location
from django.contrib.gis.admin import OSMGeoAdmin
# # Register your models here.

admin.site.register(Pipeline, OSMGeoAdmin)
admin.site.register(PipelineFile)

admin.site.register(StorageUnit, OSMGeoAdmin)
admin.site.register(StorageUnitFile)

admin.site.register(GateValve, OSMGeoAdmin)
admin.site.register( GateValveFile)

admin.site.register(TubeWell, OSMGeoAdmin)
admin.site.register(TubeWellFile)

admin.site.register(Task,  OSMGeoAdmin)
admin.site.register(Location)