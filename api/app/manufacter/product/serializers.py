import base64

from django.core.files.base import ContentFile
from rest_framework import serializers

from app.models import ProductCompany


class ImageBase64Field(serializers.ImageField):
    def to_internal_value(self, data):
        image_data = data['data']
        image_name = data['name']
        data_file = None
        if image_data.startswith('data:image'):
            format, imgstr = image_data.split(';base64,')
            data_file = ContentFile(base64.b64decode(imgstr), name=image_name)
        return super().to_internal_value(data_file)


class ProductSerializer(serializers.ModelSerializer):
    photo = ImageBase64Field(required=False)

    class Meta:
        model = ProductCompany
        exclude = ('company',)

    def create(self, validated_data):
        company = self.context['company']
        return super().create({**validated_data, 'company': company})
