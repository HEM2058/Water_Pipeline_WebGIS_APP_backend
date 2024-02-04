from django.contrib.gis.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
import json
from django.contrib.gis.geos import GEOSGeometry

class GeoData(models.Model):
    geometry = models.GeometryField(null=True)
    name = models.CharField(max_length=255, null=True)
    diameter = models.IntegerField(null=True)
    
    def __str__(self):
        return f"{self.name} m"

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

            for feature in features:
                geometry = feature.get('geometry', {})
                geometry_type = geometry.get('type')
                coordinates = geometry.get('coordinates', [])

                # Extract attribute information
                properties = feature.get('properties', {})
                name = properties.get('name')
                diameter = properties.get('diameter')

                print(f"Extracted geometry type: {geometry_type}, coordinates: {coordinates}, name: {name}, diameter: {diameter}")

                # Create a GeoData object for each feature
                geo_data = GeoData.objects.create(
                    geometry=GEOSGeometry(json.dumps({
                        "type": geometry_type,
                        "coordinates": coordinates
                    })),
                    name=name,
                    diameter=diameter
                )
                
                print(f"Saved GeoData object with ID: {geo_data.id}")
