from rest_framework import serializers

from app.models import PointInCity


class PointInCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = PointInCity
        exclude = ('company',)

    def create(self, validated_data):
        company = self.context['user']
        return super().create({**validated_data, 'company': company})
