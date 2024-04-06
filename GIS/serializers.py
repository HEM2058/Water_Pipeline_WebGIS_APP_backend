# serializers.py
from rest_framework import serializers
from .models import Pipeline ,StorageUnit, GateValve, TubeWell, Task, Location
from django.db.models import Count

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

class LocationSerializer(serializers.ModelSerializer):
    total_issues = serializers.SerializerMethodField()
    issue_counts = serializers.SerializerMethodField()

    class Meta:
        model = Location
        fields = ['total_issues', 'issue_counts']

    def get_total_issues(self, obj):
        # Get the total count of all issues
        total_issues = Location.objects.count()
        return total_issues

    def get_issue_counts(self, obj):
        # Get the count of objects for each issue type
        issue_counts = Location.objects.values('issue_type').annotate(count=Count('issue_type'))
        return issue_counts

class TaskSerializerCount(serializers.ModelSerializer):
    total_tasks = serializers.SerializerMethodField()
    task_counts = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ['total_tasks', 'task_counts']

    def get_total_tasks(self, obj):
        # Get the total count of all tasks
        total_tasks = Task.objects.count()
        return total_tasks

    def get_task_counts(self, obj):
        # Get the count of tasks for each status
        task_counts = Task.objects.values('status').annotate(count=Count('status'))
        return task_counts