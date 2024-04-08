from rest_framework import serializers

from api.app.manufacter.product.serializers import ProductSerializer
from app.models import PointInCity, ProductInWarehouse


class PointInCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = PointInCity
        exclude = ('company',)

    def create(self, validated_data):
        company = self.context['user']
        return super().create({**validated_data, 'company': company})


class ProductInWarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductInWarehouse
        exclude = ('warehouse', 'product')

    def create(self, validated_data):
        warehouse = self.context['warehouse']
        product = self.context['product']
        return super().create({**validated_data, 'warehouse': warehouse, 'product': product})


class ProductInWarehouseDetailSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = ProductInWarehouse
        exclude = ('warehouse',)
