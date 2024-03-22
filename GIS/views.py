# views.py
from rest_framework import generics
from .models import Pipeline ,StorageUnit, GateValve, TubeWell, Task
from .serializers import PipelineSerializer, StorageUnitSerializer, GateValveSerializer, TubeSerializer, TaskSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.gis.geos import GEOSGeometry
from django.core.serializers import serialize
import json
from .tasks import update_task_status  # Import the Celery task
# class PipelineListAPIView(generics.ListAPIView):
#     queryset = Pipeline.objects.all()
#     serializer_class = GeoDataSerializer


class PipelineGeoJSONAPIView(APIView):
    def get(self, request, *args, **kwargs):
        # Query Pipeline objects
        pipelines = Pipeline.objects.all()

        # Convert Pipeline queryset to GeoJSON format
        features = []
        for pipeline in pipelines:
            geometry = json.loads(pipeline.geometry.geojson)
            
            feature = {
                "type": "Feature",
                "geometry": geometry,
                "properties": {
                    "id": pipeline.id,
                    "diameter_m": pipeline.Diameter_m,  # Change field name accordingly
                    "material": pipeline.Material,
                    "length_m": pipeline.Length_m,
                    "flow_rate": pipeline.Flow_Rate,
                    "installation_date": pipeline.Installation_date.isoformat() if pipeline.Installation_date else None,
                    "condition": pipeline.Condition,
                    "leakage": pipeline.Leakage,
                }
            }
            features.append(feature)

        feature_collection = {
            "type": "FeatureCollection",
            "features": features,
        }

        return Response(feature_collection)

class StorageUnitGeoJSONAPIView(APIView):
    def get(self, request, *args, **kwargs):
        # Query StorageUnit objects
        storage_units = StorageUnit.objects.all()

        # Convert StorageUnit queryset to GeoJSON format
        features = []
        for unit in storage_units:
            # Assuming you have geometry field in StorageUnit model, adjust this accordingly
            geometry = json.loads(unit.geometry.geojson)
            
            feature = {
                "type": "Feature",
                "geometry": geometry,
                "properties": {
                    "id": unit.id,
                    "Type": unit.Type,
                    "Capacity": unit.Capacity,
                    "Usage": unit.Usage,
                    "Condition": unit.Condition,
                    "Name": unit.Name,
                }
            }
            features.append(feature)

        feature_collection = {
            "type": "FeatureCollection",
            "features": features,
        }

        return Response(feature_collection)

class GateValveGeoJSONAPIView(APIView):
    def get(self, request, *args, **kwargs):
        # Query GateValve objects
        gate_valves = GateValve.objects.all()

        # Convert GateValve queryset to GeoJSON format
        features = []
        for valve in gate_valves:
            # Assuming you have geometry field in GateValve model, adjust this accordingly
            geometry = json.loads(valve.geometry.geojson)
            
            feature = {
                "type": "Feature",
                "geometry": geometry,
                "properties": {
                    "id": valve.id,
                    "Material": valve.Material,
                    "Status": valve.Status,
                    "Installation_date": valve.Installation_date.isoformat() if valve.Installation_date else None,
                }
            }
            features.append(feature)

        feature_collection = {
            "type": "FeatureCollection",
            "features": features,
        }

        return Response(feature_collection)

class TubeWellGeoJSONAPIView(APIView):
    def get(self, request, *args, **kwargs):
        # Query TubeWell objects
        tubewells = TubeWell.objects.all()

        # Convert TubeWell queryset to GeoJSON format
        features = []
        for well in tubewells:
            # Assuming you have geometry field in TubeWell model, adjust this accordingly
            geometry = json.loads(well.geometry.geojson)
            
            feature = {
                "type": "Feature",
                "geometry": geometry,
                "properties": {
                    "id": well.id,
                    "Name": well.Name,
                    "Pump_Type": well.Pump_Type,
                    "Depth": well.Depth,
                    "Flow_Rate": well.Flow_Rate,
                    "Condition": well.Condition,
                }
            }
            features.append(feature)

        feature_collection = {
            "type": "FeatureCollection",
            "features": features,
        }

        return Response(feature_collection)

class TaskView(generics.ListAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    def list(self, request, *args, **kwargs):
        # Call the Celery task to update task statuses
        update_task_status()
        return super().list(request, *args, **kwargs)

# class CentroidPolygonView(APIView):
#     def get(self, request, *args, **kwargs):
#         selected_name = request.GET.get('selectedName', None)

#         if selected_name:
#             try:
#                 geo_data = GeoData.objects.get(name=selected_name)
#                 geometry = geo_data.geometry
#                 if geometry.geom_type == 'Polygon':
#                     centroid = geometry.centroid
#                     print(f'Centroid Coordinates: {centroid}')
#                     # Now, you can process further or send the response if needed.
#                     return Response({'centroid': str(centroid)})
#                 else:
#                     print('Selected feature is not a Polygon')
#                     # Handle the case where the feature is not a Polygon
#                     return Response({'error': 'Selected feature is not a Polygon'}, status=400)
#             except GeoData.DoesNotExist:
#                 print('Feature not found')
#                 # Handle the case where the feature is not found
#                 return Response({'error': 'Feature not found'}, status=404)
#         else:
#             print('Please provide a valid selectedName parameter')
#             # Handle the case where selectedName parameter is not provided or invalid
#             return Response({'error': 'Please provide a valid selectedName parameter'}, status=400)