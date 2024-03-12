from django.urls import path
from .views import PipelineGeoJSONAPIView, StorageUnitGeoJSONAPIView, GateValveGeoJSONAPIView, TubeWellGeoJSONAPIView

urlpatterns = [
    path('pipeline-geojson/', PipelineGeoJSONAPIView.as_view(), name='pipeline_geojson'),
    path('storage-unit-geojson/', StorageUnitGeoJSONAPIView.as_view(), name='storage_unit_geojson'),
    path('gate-valve-geojson/', GateValveGeoJSONAPIView.as_view(), name='gate_valve_geojson'),
    path('tube-well-geojson/', TubeWellGeoJSONAPIView.as_view(), name='tube_well_geojson'),
]
