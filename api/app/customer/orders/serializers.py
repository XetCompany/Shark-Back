from rest_framework import serializers

from api.app.common.serializers import ProductCompanySerializer
from api.app.customer.serializers import GroupPathsSerializer
from app.models import Order, OrderProduct


class OrderProductSerializer(serializers.ModelSerializer):
    product = ProductCompanySerializer()

    class Meta:
        model = OrderProduct
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    products = OrderProductSerializer(many=True)
    group_paths = GroupPathsSerializer(many=True)

    class Meta:
        model = Order
        exclude = ('user',)
