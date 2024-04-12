from rest_framework import serializers

from api.app.common.serializers import (
    ProductCompanySerializer, CitySerializer,
)
from api.app.customer.products.utils import user_can_comment_product, user_can_add_product_to_cart
from app.models import Path, GroupPaths, SearchInfo, GroupPath


class PathSerializer(serializers.ModelSerializer):
    point_a = CitySerializer()
    point_b = CitySerializer()

    class Meta:
        model = Path
        fields = '__all__'


class GroupPathSerializer(serializers.ModelSerializer):
    path = PathSerializer()

    def to_representation(self, instance):
        data = super().to_representation(instance)

        if data['is_reversed']:
            data['path']['point_a'], data['path']['point_b'] = data['path']['point_b'], data['path']['point_a']

        data.pop('is_reversed')

        return data

    class Meta:
        model = GroupPath
        exclude = ('id',)


class GroupPathsSerializer(serializers.ModelSerializer):
    paths = GroupPathSerializer(many=True)
    product = ProductCompanySerializer()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.is_instant_delivery and instance.instant_city:
            instant_path = PathSerializer(
                data={
                    'point_a': CitySerializer(instance=instance.instant_city).data,
                    'point_b': CitySerializer(instance=instance.instant_city).data,
                    'length': 0,
                    'time': 0,
                    'price': 0,
                    'type': 'instant',
                },
            )
            instant_path.is_valid()
            instant_group_path = GroupPathSerializer(
                data={
                    'path': instant_path.data,
                    'is_reversed': False,
                },
            )
            instant_group_path.is_valid()
            data['paths'].append(instant_group_path.data)
        return data

    class Meta:
        model = GroupPaths
        exclude = ('id', 'is_instant_delivery', 'instant_city')


class SearchInfoSerializer(serializers.ModelSerializer):
    groups_paths = GroupPathsSerializer(many=True)

    class Meta:
        model = SearchInfo
        exclude = ('user',)


class ProductCompanyCustomerSerializer(ProductCompanySerializer):
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['is_need_comment'] = user_can_comment_product(self.context['user'], instance)
        data['is_can_add_to_cart'] = user_can_add_product_to_cart(self.context['user'], instance)
        return data
