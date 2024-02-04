# urls.py
from django.urls import path
from .views import GeoDataListAPIView

urlpatterns = [
    path('api/geo-data/', GeoDataListAPIView.as_view(), name='geo-data-list'),
    # Add other URLs as needed
]
