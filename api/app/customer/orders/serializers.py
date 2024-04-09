from rest_framework import serializers

from api.app.common.serializers import ProductCompanySerializer
from api.app.customer.serializers import GroupPathsSerializer
from app.models import Order, OrderProduct, OrderStatus


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


class OrderEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('status', 'decline_reason')

    def validate_status(self, value):
        order = self.context['order']
        if order.status != OrderStatus.AWAITING:
            raise serializers.ValidationError('Order status is not awaiting')

        if value not in [OrderStatus.ADOPTED, OrderStatus.DECLINED]:
            raise serializers.ValidationError('Invalid status')

        return value

    def validate(self, attrs):
        if attrs['status'] == OrderStatus.DECLINED and not attrs.get('decline_reason'):
            raise serializers.ValidationError('Decline reason is required')

        return attrs
