from rest_framework import serializers

from app.models import ProductCompany


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCompany
        exclude = ('company',)

    def create(self, validated_data):
        company = self.context['company']
        return super().create({**validated_data, 'company': company})
