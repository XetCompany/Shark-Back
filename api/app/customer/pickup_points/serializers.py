from rest_framework import serializers

from api.app.customer.serializers import CitySerializer
from app.models import PointInCity


class PointInCitySerializer(serializers.ModelSerializer):
    city = CitySerializer()

    class Meta:
        model = PointInCity
        fields = ('id', 'city')
