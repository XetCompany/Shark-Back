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

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['total_price'] = sum([float(product['product']['price']) * product['count'] for product in data['products']])
        data['avg_price'] = data['total_price'] / sum([product['count'] for product in data['products']])
        return data

    class Meta:
        model = Order
        exclude = ('user',)


class OrderEditSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(choices=(
        (OrderStatus.ADOPTED, 'Принят'),
        (OrderStatus.DECLINED, 'Отклонен'),
    ))
    decline_reason = serializers.CharField(required=False)

    class Meta:
        model = Order
        fields = ('status', 'decline_reason')

    def validate_status(self, value):
        if not value:
            raise serializers.ValidationError('Status is required')

        order = self.context['order']
        if order.status != OrderStatus.AWAITING:
            raise serializers.ValidationError('Order status is not awaiting')

        return value

    def validate(self, attrs):
        if attrs['status'] == OrderStatus.DECLINED and not attrs.get('decline_reason'):
            raise serializers.ValidationError('Decline reason is required')

        return attrs
