# views.py
from rest_framework import generics
from .models import Pipeline ,StorageUnit, GateValve, TubeWell, Task
from .serializers import PipelineSerializer, StorageUnitSerializer, GateValveSerializer, TubeSerializer, TaskSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.gis.geos import GEOSGeometry
from django.core.serializers import serialize
import json
from sentinelhub import SentinelHubRequest, DataCollection, MimeType, CRS, SHConfig, BBox
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


#Fetching the route elevation from sentinel api

class ElevationAPIView(APIView):
    def post(self, request):
        # Credentials
        config = SHConfig()
        config.sh_client_id = '80cb4233-97cd-4ae8-aa82-787cc091082f'
        config.sh_client_secret = 'Oh48OTexSh32T4InF8fBje5BGvnAYH6i'

        # Get coordinates from request data
        coordinates = request.data.get('coordinates', [])
        print("====================================================================")
        print(coordinates)
        elevation_data = []

        # Function to get elevation value for a single location
        def get_elevation(latitude, longitude):
            # Define bounding box around the point of interest
            bbox = BBox(bbox=[
                longitude - 0.0001,  # left
                latitude - 0.0001,   # bottom
                longitude + 0.0001,  # right
                latitude + 0.0001    # top
            ], crs=CRS.WGS84)

            # Create SentinelHub request for elevation data
            request_elevation = SentinelHubRequest(
                evalscript="""
                    //VERSION=3
                    function setup() {
                        return {
                            input: [{
                                bands: ["DEM"]
                            }],
                            output: {
                                bands: 1,
                                sampleType: "FLOAT32"
                            }
                        };
                    }

                    function evaluatePixel(sample) {
                        return [sample.DEM];
                    }
                """,
                input_data=[
                    SentinelHubRequest.input_data(
                        data_collection=DataCollection.DEM,
                    ),
                ],
                responses=[
                    SentinelHubRequest.output_response('default', MimeType.TIFF),
                ],
                bbox=bbox,
                size=[1, 1],  # Set size to 1x1 pixel to get only one pixel value
                config=config,
            )

            # Get elevation data from the request
            elevation_response = request_elevation.get_data()

            # Extract elevation value
            elevation_value = elevation_response[0][0][0]
            print(elevation_value)

            return elevation_value

        # Fetch elevation values for all coordinates
        for longitude, latitude in coordinates:
            print(latitude)
            print(longitude)
            elevation = get_elevation(latitude, longitude)
            elevation_data.append({'latitude': latitude, 'longitude': longitude, 'elevation': elevation})

        return Response({'elevation_data': elevation_data})