from rest_framework import serializers

from api.app.common.serializers import ProductCompanySerializer, UserInfoSerializer
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
    user = UserInfoSerializer()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['total_price'] = sum([float(product['product']['price']) * product['count'] for product in data['products']])
        data['total_count'] = sum([product['count'] for product in data['products']])

        data['total_path_length'] = sum([float(path['path']['length']) for group_path in data['group_paths'] for path in group_path['paths']])
        data['total_path_price'] = sum([float(path['path']['price']) for group_path in data['group_paths'] for path in group_path['paths']])
        data['total_path_time'] = sum([path['path']['time'] for group_path in data['group_paths'] for path in group_path['paths']])

        return data

    class Meta:
        model = Order
        fields = '__all__'


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
