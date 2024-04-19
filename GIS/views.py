# views.py
from rest_framework import generics
from .models import Pipeline ,StorageUnit, GateValve, TubeWell, Task, Location
from .serializers import PipelineSerializer, StorageUnitSerializer, GateValveSerializer, TubeSerializer, TaskSerializer, LocationSerializer,TaskSerializerCount,IssueSerializer,IssueGeoprocessingSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.gis.geos import GEOSGeometry
from django.core.serializers import serialize
import json
from sentinelhub import SentinelHubRequest, DataCollection, MimeType, CRS, SHConfig, BBox
from .tasks import update_task_status  # Import the Celery task
from django.db.models import Count
from rest_framework.decorators import api_view
from rest_framework import status
from django.contrib.auth.decorators import login_required
import random
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

#Issues count fetching api

class LocationIssueCountAPI(APIView):
    def get(self, request):
        # Get the total count of all issues
        total_issues = Location.objects.count()
        
        # Get the count of objects for each issue type
        issue_counts = Location.objects.values('issue_type').annotate(count=Count('issue_type'))

        # Serialize the data
        serializer = LocationSerializer({
            'total_issues': total_issues,
            'issue_counts': issue_counts
        })

        return Response(serializer.data)

#Task count feching api
class TaskListAPI(APIView):
    def get(self, request):
        tasks = Task.objects.all()
        serializer = TaskSerializerCount(tasks, context={'request': request})
        return Response(serializer.data)
#Fetchin all the issues

class IssuesListApi(generics.ListAPIView):
    serializer_class = IssueSerializer
    queryset = Location.objects.all()

class CreateLocationAPIView(generics.CreateAPIView):
    queryset = Location.objects.all()
    serializer_class = IssueGeoprocessingSerializer

    def perform_create(self, serializer):
        # Extract geometry data from request
        geometry_data = self.request.data.get('geometry', {})
        print(geometry_data)
        
        # Construct a GEOSGeometry object
        if geometry_data:
            geometry = GEOSGeometry(json.dumps(geometry_data))
            # Assign the constructed geometry to the serializer
            serializer.validated_data['geometry'] = geometry

        instance = serializer.save()
        print(instance)

        # Perform proximity analysis and mark the nearest pipeline as leakage
        instance.find_nearest_pipeline()
        print("after find nearest")

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class IssueLocation(generics.ListAPIView):
    queryset = Location.objects.all()
    serializer_class = IssueGeoprocessingSerializer


class OptimumRouteFinder(APIView):
    ACCESS_TOKEN = "1b0d6442-4806-4a6c-90bb-5437128096eb"
    ROUTING_API_URL = "https://route-init.gallimap.com/api/v1/routing?mode=driving&srcLat={src_lat}&srcLng={src_lng}&dstLat={dst_lat}&dstLng={dst_lng}&accessToken={access_token}"

    def post(self, request):
        # Receive destination coordinate point from the user
        destination = request.data.get('destination')
        destination_point = Point(destination['longitude'], destination['latitude'], srid=4326)

        # Define a buffer distance (in meters) to find nearby pipelines
        buffer_distance = 200  # Adjust according to your requirements

        # Use spatial query to find nearby pipelines within the buffer distance
        nearby_pipelines = Pipeline.objects.filter(geometry__distance_lte=(destination_point, buffer_distance))

        # Initialize variables to store the shortest feasible route and its elevation
        shortest_feasible_route = None
        min_elevation_difference = float('inf')

        # Iterate through nearby pipelines
        for pipeline in nearby_pipelines:
            # Sample points along the pipeline
            sampled_points = self.sample_points_on_pipeline(pipeline.geometry)

            # Make the routing API request for each sampled source coordinate and the given destination coordinate
            for source_coordinate in sampled_points:
                response = self.make_routing_request(source_coordinate, (destination['longitude'], destination['latitude']))

                # Extract route and distance from the response
                route = response['route']
                distance = response['distance']

                # Check if the distance is shorter than the current shortest feasible route
                if distance < min_elevation_difference:
                    # Calculate elevation difference for the route
                    elevation_difference = self.calculate_elevation_difference(route)

                    # If the route is feasible (i.e., water flows from high to low elevation), update shortest_feasible_route
                    if elevation_difference >= 0:
                        shortest_feasible_route = route
                        min_elevation_difference = distance

        if shortest_feasible_route:
            return Response({'optimum_route': shortest_feasible_route})
        else:
            return Response({'message': 'No feasible route found'})

    def sample_points_on_pipeline(self, pipeline_geometry, num_points=3):
        """
        Sample points along the pipeline geometry.
        """
        sampled_points = []
        num_points = min(num_points, pipeline_geometry.num_points)
        for _ in range(num_points):
            # Sample a random point index along the pipeline
            random_index = random.randint(0, pipeline_geometry.num_points - 1)
            # Extract the coordinates of the sampled point
            sampled_point = pipeline_geometry[random_index]
            sampled_points.append(sampled_point.coords)
        return sampled_points

    def make_routing_request(self, source, destination):
        # Format the routing API URL with source, destination, and access token
        routing_api_url = self.ROUTING_API_URL.format(
            src_lat=source[1],  # Assuming source is (longitude, latitude)
            src_lng=source[0],
            dst_lat=destination[1],
            dst_lng=destination[0],
            access_token=self.ACCESS_TOKEN
        )

        # Send a GET request to the routing API URL
        response = requests.get(routing_api_url)
        return response.json()

    def calculate_elevation_difference(self, route):
        # Extract coordinates from the route
        coordinates = [(step['longitude'], step['latitude']) for step in route]

        # Request elevation data for the coordinates
        elevation_data = self.request_elevation_data(coordinates)

        # Calculate elevation difference along the route
        elevation_difference = 0
        for i in range(len(elevation_data) - 1):
            elevation_difference += elevation_data[i + 1]['elevation'] - elevation_data[i]['elevation']

        return elevation_difference

    def request_elevation_data(self, coordinates):
        # Credentials
        config = SHConfig()
        config.sh_client_id = '80cb4233-97cd-4ae8-aa82-787cc091082f'
        config.sh_client_secret = 'Oh48OTexSh32T4InF8fBje5BGvnAYH6i'

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

            return elevation_value

        # Fetch elevation values for all coordinates
        for longitude, latitude in coordinates:
            elevation = get_elevation(latitude, longitude)
            elevation_data.append({'latitude': latitude, 'longitude': longitude, 'elevation': elevation})

        return elevation_data
