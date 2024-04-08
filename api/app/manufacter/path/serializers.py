from rest_framework import serializers

from app.models import Path, City


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class PathCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Path
        fields = '__all__'


class PathSerializer(serializers.ModelSerializer):
    class Meta:
        model = Path
        fields = '__all__'
        read_only_fields = ('point_a', 'point_b')


class PathInfoSerializer(serializers.ModelSerializer):
    point_a = CitySerializer()
    point_b = CitySerializer()

    class Meta:
        model = Path
        fields = '__all__'
