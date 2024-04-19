from django.urls import path
from .views import PipelineGeoJSONAPIView, StorageUnitGeoJSONAPIView, GateValveGeoJSONAPIView, TubeWellGeoJSONAPIView, TaskView, ElevationAPIView,LocationIssueCountAPI,TaskListAPI,IssuesListApi,CreateLocationAPIView,IssueLocation,OptimumRouteFinder

urlpatterns = [
    path('pipeline-geojson/', PipelineGeoJSONAPIView.as_view(), name='pipeline_geojson'),
    path('storage-unit-geojson/', StorageUnitGeoJSONAPIView.as_view(), name='storage_unit_geojson'),
    path('gate-valve-geojson/', GateValveGeoJSONAPIView.as_view(), name='gate_valve_geojson'),
    path('tube-well-geojson/', TubeWellGeoJSONAPIView.as_view(), name='tube_well_geojson'),
    path('tasks/',TaskView.as_view(), name="tasks"),
    path('elevation/', ElevationAPIView.as_view(), name='elevation_api'),
    path('location/issue-count/', LocationIssueCountAPI.as_view(), name='location_issue_count_api'),
    path('tasks/count', TaskListAPI.as_view(), name='task-list'),
    path('issues/',IssuesListApi.as_view(), name='issues'),
    path('issues-location/', CreateLocationAPIView.as_view(), name='issues-location'),
    path('issues-view/',IssueLocation.as_view(),name='issues-view'),
    path('OptimumRouteFinder/',OptimumRouteFinder.as_view(),name='optimum-route')

 
]
