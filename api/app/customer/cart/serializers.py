from rest_framework import serializers

from api.app.common.serializers import ProductCompanySerializer
from app.models import CartProduct, SearchInfo, GroupPaths, Path, City


class CartProductSerializer(serializers.ModelSerializer):
    product = ProductCompanySerializer()

    class Meta:
        model = CartProduct
        exclude = ('id',)


class CartProductAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartProduct
        exclude = ('id', 'product',)

    def validate(self, attrs):
        cart = self.context['cart']
        product = self.context['product']
        is_exist = cart.products.filter(product=product).exists()
        if is_exist:
            raise serializers.ValidationError('Product already in cart')

        # TODO: возможно убрать, если будет время
        first_cart_product = cart.products.first()
        if first_cart_product:
            if first_cart_product.product.company != product.company:
                raise serializers.ValidationError('You can not add products from different companies to cart')

        return attrs

    def create(self, validated_data):
        product = self.context['product']
        product = CartProduct.objects.create(product=product, **validated_data)
        return product


class CartProductUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartProduct
        exclude = ('id', 'product',)


