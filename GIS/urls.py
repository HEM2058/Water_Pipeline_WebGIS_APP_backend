# urls.py
from django.urls import path
from .views import GeoDataListAPIView, GeoJSONAPIView

urlpatterns = [
    path('geo-data/', GeoDataListAPIView.as_view(), name='geo-data-list'),
      path('geo-json/', GeoJSONAPIView.as_view(), name='geo-json'),
    # Add other URLs as needed
]
