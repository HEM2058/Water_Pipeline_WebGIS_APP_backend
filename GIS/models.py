from django.contrib.gis.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
import json
from django.contrib.gis.geos import GEOSGeometry

#model for pipeline 

class Pipeline(models.Model):
    Diameter_m = models.IntegerField()
    Material = models.CharField(max_length=50)
    Length_m = models.FloatField(default=0)
    Flow_Rate = models.FloatField()
    Installation_date = models.DateField(null=True, blank=True)
    Condition = models.CharField(max_length=50)
    Leakage = models.BooleanField()

    def __str__(self):
        return f"Diameter: {self.Diameter_m}, Material: {self.Material}, Flow Rate: {self.Flow_Rate_} m^3/s, Condition: {self.Condition}, Leakage: {self.Leakage}"

class PipelineFile(models.Model):
    file = models.FileField(upload_to='pipeline_files/')

@receiver(post_save, sender=PipelineFile)
def extract_pipeline_data(sender, instance, **kwargs):
    if instance.file.name.endswith('.geojson'):
        print(f"Processing GeoJSON file: {instance.file.name}")
        
        with open(instance.file.path, 'r') as geojson_file:
            # Print the content of the GeoJSON file
            geojson_content = geojson_file.read()
            print(f"GeoJSON Content: {geojson_content}")
            
            data = json.loads(geojson_content)
            features = data.get('features', [])

            for feature in features:
                properties = feature.get('properties', {})
                diameter = properties.get('Diameter_m')
                material = properties.get('Material')
                length = properties.get('Length_m')
                flow_rate = properties.get('Flow_Rate_')
                installation_date = properties.get('Installation_date')
                condition = properties.get('Condition')
                leakage = properties.get('Leakage')

                print(f"Diameter: {diameter}, Material: {material}, Length: {length}, Flow Rate: {flow_rate}, Installation Date: {installation_date}, Condition: {condition}, Leakage: {leakage}")

                # Create a Pipeline object for each feature
                pipeline = Pipeline.objects.create(
                    Diameter_m=diameter,
                    Material=material,
                    Length_m=length,
                    Flow_Rate_=flow_rate,
                    Installation_date=installation_date,
                    Condition=condition,
                    Leakage=leakage
                )
                
                print(f"Saved Pipeline object with ID: {pipeline.id}")

#model for the storage-unit

class StorageUnit(models.Model):
    Type = models.CharField(max_length=50)
    Capacity = models.FloatField(default=0)
    Usage = models.FloatField(default=0)
    Condition = models.CharField(max_length=50, null=True)
    Name = models.CharField(max_length=255)

    def __str__(self):
        return f"Type: {self.Type}, Capacity: {self.Capacity}, Usage: {self.Usage_}, Condition: {self.Condition}, Name: {self.Name}"

class StorageUnitFile(models.Model):
    file = models.FileField(upload_to='storage_unit_files/')

@receiver(post_save, sender=StorageUnitFile)
def extract_storage_unit_data(sender, instance, **kwargs):
    if instance.file.name.endswith('.geojson'):
        print(f"Processing GeoJSON file: {instance.file.name}")
        
        with open(instance.file.path, 'r') as geojson_file:
            # Print the content of the GeoJSON file
            geojson_content = geojson_file.read()
            print(f"GeoJSON Content: {geojson_content}")
            
            data = json.loads(geojson_content)
            features = data.get('features', [])

            for feature in features:
                properties = feature.get('properties', {})
                unit_type = properties.get('Type')
                capacity = properties.get('Capacity')
                usage = properties.get('Usage_')
                condition = properties.get('Condition')
                name = properties.get('Name')

                print(f"Type: {unit_type}, Capacity: {capacity}, Usage: {usage}, Condition: {condition}, Name: {name}")

                # Create a StorageUnit object for each feature
                storage_unit = StorageUnit.objects.create(
                    Type=unit_type,
                    Capacity=capacity,
                    Usage_=usage,
                    Condition=condition,
                    Name=name
                )
                
                print(f"Saved StorageUnit object with ID: {storage_unit.id}")

#model for the gatevalve

class GateValve(models.Model):
    Material = models.CharField(max_length=50, null=True)
    Status = models.CharField(max_length=10, null=True)
    Installation_date = models.DateField(null=True)

    def __str__(self):
        return f"Material: {self.Material}, Status: {self.Status}, Installation Date: {self.Installation_date}"

class GateValveFile(models.Model):
    file = models.FileField(upload_to='gatevalve_files/')

@receiver(post_save, sender=GateValveFile)
def extract_gate_valve_data(sender, instance, **kwargs):
    if instance.file.name.endswith('.geojson'):
        print(f"Processing GeoJSON file: {instance.file.name}")
        
        with open(instance.file.path, 'r') as geojson_file:
            # Print the content of the GeoJSON file
            geojson_content = geojson_file.read()
            print(f"GeoJSON Content: {geojson_content}")
            
            data = json.loads(geojson_content)
            features = data.get('features', [])

            for feature in features:
                properties = feature.get('properties', {})
                material = properties.get('Material')
                status = properties.get('Status')
                installation_date = properties.get('Installati')

                print(f"Material: {material}, Status: {status}, Installation Date: {installation_date}")

                # Create a GateValve object for each feature
                gate_valve = GateValve.objects.create(
                    Material=material,
                    Status=status,
                    Installation_date=installation_date
                )
                
                print(f"Saved GateValve object with ID: {gate_valve.id}")


class TubeWell(models.Model):
    Name = models.CharField(max_length=100)
    Pump_Type = models.CharField(max_length=50, null=True)
    Depth = models.FloatField(default=0)
    Flow_Rate = models.FloatField(default=0)
    Condition = models.CharField(max_length=50, null=True)

    def __str__(self):
        return f"Name: {self.Name}, Pump Type: {self.Pump_Type}, Depth: {self.Depth}, Flow Rate: {self.Flow_Rate}, Condition: {self.Condition}"

class TubeWellFile(models.Model):
    file = models.FileField(upload_to='tubewell_files/')

@receiver(post_save, sender=TubeWellFile)
def extract_tubewell_data(sender, instance, **kwargs):
    if instance.file.name.endswith('.geojson'):
        print(f"Processing GeoJSON file: {instance.file.name}")
        
        with open(instance.file.path, 'r') as geojson_file:
            # Print the content of the GeoJSON file
            geojson_content = geojson_file.read()
            print(f"GeoJSON Content: {geojson_content}")
            
            data = json.loads(geojson_content)
            features = data.get('features', [])

            for feature in features:
                properties = feature.get('properties', {})
                name = properties.get('Name')
                pump_type = properties.get('Pump_Type')
                depth = properties.get('Depth')
                flow_rate = properties.get('Flow_Rate')
                condition = properties.get('Condition')

                print(f"Name: {name}, Pump Type: {pump_type}, Depth: {depth}, Flow Rate: {flow_rate}, Condition: {condition}")

                # Create a TubeWell object for each feature
                tubewell = TubeWell.objects.create(
                    Name=name,
                    Pump_Type=pump_type,
                    Depth=depth,
                    Flow_Rate=flow_rate,
                    Condition=condition
                )
                
                print(f"Saved TubeWell object with ID: {tubewell.id}")