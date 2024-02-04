from django.contrib.gis.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
import json
from django.contrib.gis.geos import GEOSGeometry

class GeoData(models.Model):
    geometry_collection = models.GeometryCollectionField()

class GeoJSONFile(models.Model):
    file = models.FileField(upload_to='geojson_files/')

@receiver(post_save, sender=GeoJSONFile)
def extract_geojson_features(sender, instance, **kwargs):
    if instance.file.name.endswith('.geojson'):
        print(f"Processing GeoJSON file: {instance.file.name}")
        
        with open(instance.file.path, 'r') as geojson_file:
            # Print the content of the GeoJSON file
            geojson_content = geojson_file.read()
            print(f"GeoJSON Content: {geojson_content}")
            
            data = json.loads(geojson_content)
            features = data.get('features', [])

            geometry_collection = {
                "type": "GeometryCollection",
                "geometries": []
            }

            for feature in features:
                geometry = feature.get('geometry', {})
                geometry_type = geometry.get('type')
                coordinates = geometry.get('coordinates', [])

                print(f"Extracted geometry type: {geometry_type}, coordinates: {coordinates}")

                # Append the geometry to the collection
                geometry_collection['geometries'].append({
                    "type": geometry_type,
                    "coordinates": coordinates
                })

            # Convert the collection to a GeoJSON string
            geojson_string = json.dumps(geometry_collection)

            print(f"GeoJSON String: {geojson_string}")

            # Create a GEOSGeometry object from the GeoJSON string
            geo_data = GeoData.objects.create(geometry_collection=GEOSGeometry(geojson_string))
            print(f"Saved GeoData object with ID: {geo_data.id}")



