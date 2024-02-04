# views.py
from rest_framework import generics
from .models import GeoData
from .serializers import GeoDataSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.gis.geos import GEOSGeometry
from django.core.serializers import serialize
import json

class GeoDataListAPIView(generics.ListAPIView):
    queryset = GeoData.objects.all()
    serializer_class = GeoDataSerializer


class GeoJSONAPIView(APIView):
    def get(self, request, *args, **kwargs):
        # Query GeoData objects
        geo_data = GeoData.objects.all()

        # Convert GeoData queryset to GeoJSON format
        features = []
        for data in geo_data:
            geometry = json.loads(data.geometry.geojson)
            
            feature = {
                "type": "Feature",
                "geometry": geometry,
                "properties": {
                    "id": data.id,
                    "name": data.name,
                    "diameter": data.diameter,
                }
            }
            features.append(feature)

        feature_collection = {
            "type": "FeatureCollection",
            "features": features,
        }

        return Response(feature_collection)