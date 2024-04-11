from rest_framework import serializers

from api.app.common.fields import FileBase64Field
from app.models import ProductCompany


class ProductSerializer(serializers.ModelSerializer):
    photo = FileBase64Field(required=False, base64_type='image')

    class Meta:
        model = ProductCompany
        exclude = ('company',)

    def create(self, validated_data):
        company = self.context['company']
        return super().create({**validated_data, 'company': company})
