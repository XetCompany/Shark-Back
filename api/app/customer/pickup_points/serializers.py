from rest_framework import serializers

from api.app.common.serializers import CitySerializer
from app.models import PointInCity


class PickupPointSerializer(serializers.ModelSerializer):
    city = CitySerializer()

    class Meta:
        model = PointInCity
        fields = ('id', 'city')
