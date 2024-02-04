# views.py
from rest_framework import generics
from .models import GeoData
from .serializers import GeoDataSerializer

class GeoDataListAPIView(generics.ListAPIView):
    queryset = GeoData.objects.all()
    serializer_class = GeoDataSerializer
