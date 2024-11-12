from rest_framework import serializers
from .models import CarPlate

class CarPlateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarPlate
        fields = ['id', 'image', 'recognized_text', 'created_at']
        read_only_fields = ['recognized_text', 'created_at']