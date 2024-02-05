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

class CentroidPolygonView(APIView):
    def get(self, request, *args, **kwargs):
        selected_name = request.GET.get('selectedName', None)

        if selected_name:
            try:
                geo_data = GeoData.objects.get(name=selected_name)
                geometry = geo_data.geometry
                if geometry.geom_type == 'Polygon':
                    centroid = geometry.centroid
                    print(f'Centroid Coordinates: {centroid}')
                    # Now, you can process further or send the response if needed.
                    return Response({'centroid': str(centroid)})
                else:
                    print('Selected feature is not a Polygon')
                    # Handle the case where the feature is not a Polygon
                    return Response({'error': 'Selected feature is not a Polygon'}, status=400)
            except GeoData.DoesNotExist:
                print('Feature not found')
                # Handle the case where the feature is not found
                return Response({'error': 'Feature not found'}, status=404)
        else:
            print('Please provide a valid selectedName parameter')
            # Handle the case where selectedName parameter is not provided or invalid
            return Response({'error': 'Please provide a valid selectedName parameter'}, status=400)