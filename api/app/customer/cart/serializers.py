from rest_framework import serializers

from api.app.common.serializers import ProductCompanySerializer
from app.models import CartProduct


class CartProductSerializer(serializers.ModelSerializer):
    product = ProductCompanySerializer()

    class Meta:
        model = CartProduct
        exclude = ('id',)


class CartProductAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartProduct
        exclude = ('id', 'product',)

    def create(self, validated_data):
        product = self.context['product']
        product = CartProduct.objects.create(product=product, **validated_data)
        return product
