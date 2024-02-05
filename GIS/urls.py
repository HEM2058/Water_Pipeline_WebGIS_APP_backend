# urls.py
from django.urls import path
from .views import GeoDataListAPIView, GeoJSONAPIView, CentroidPolygonView

urlpatterns = [
    path('geo-data/', GeoDataListAPIView.as_view(), name='geo-data-list'),
    path('geo-json/', GeoJSONAPIView.as_view(), name='geo-json'),
    path('centroid/', CentroidPolygonView.as_view(), name='centroid_polygon'),

]
