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

    def validate(self, data):
        if data['point_a'] == data['point_b']:
            raise serializers.ValidationError('Points must be different')

        if Path.objects.filter(point_a=data['point_a'], point_b=data['point_b'], type=data['type']).exists():
            raise serializers.ValidationError('Path already exists')
        elif Path.objects.filter(point_a=data['point_b'], point_b=data['point_a'], type=data['type']).exists():
            raise serializers.ValidationError('Path already exists')

        return data


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
