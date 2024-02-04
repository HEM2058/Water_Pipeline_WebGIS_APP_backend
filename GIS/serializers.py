# serializers.py
from rest_framework import serializers
from .models import GeoData

class GeoDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeoData
        fields = '__all__'
