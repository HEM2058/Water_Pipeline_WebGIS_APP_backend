# serializers.py
from rest_framework import serializers
from .models import Pipeline ,StorageUnit, GateValve, TubeWell, Task

class PipelineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pipeline
        fields = '__all__'
class StorageUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorageUnit
        fields = '__all__'
class GateValveSerializer(serializers.ModelSerializer):
    class Meta:
        model = GateValve
        fields = '__all__'
class TubeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TubeWell
        fields = '__all__'
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'