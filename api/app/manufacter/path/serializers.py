from django.db.models import Q
from rest_framework import serializers

from api.app.common.serializers import CitySerializer
from app.models import Path, City


class PathCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Path
        fields = '__all__'

    def validate(self, data):
        if data['point_a'] == data['point_b']:
            raise serializers.ValidationError('Points must be different')

        user = self.context['user']
        if user.paths.filter(
            Q(point_a=data['point_a'], point_b=data['point_b'], type=data['type']) |
            Q(point_a=data['point_b'], point_b=data['point_a'], type=data['type'])
        ).exists():
            raise serializers.ValidationError('Path already exists')

        return data


class PathEditSerializer(serializers.ModelSerializer):
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


class ImportExcelSerializer(serializers.Serializer):
    excel = serializers.FileField()


class PatternExcelSerializer(serializers.Serializer):
    excel = serializers.FileField()
