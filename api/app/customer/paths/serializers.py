from rest_framework import serializers


class PathsFiltersSerializer(serializers.Serializer):
    sort_by = serializers.ChoiceField(choices=(
        ('price', 'Цена'),
        ('time', 'Время'),
        ('distance', 'Расстояние'),

        ('all', 'Все'),
    ), default='price')

    is_automobile = serializers.BooleanField(default=True)
    is_railway = serializers.BooleanField(default=True)
    is_sea = serializers.BooleanField(default=True)
    is_river = serializers.BooleanField(default=True)
    is_air = serializers.BooleanField(default=True)

    min_price = serializers.CharField(required=False, allow_null=True)
    max_price = serializers.CharField(required=False, allow_null=True)
    min_time = serializers.CharField(required=False, allow_null=True)
    max_time = serializers.CharField(required=False, allow_null=True)
    min_distance = serializers.CharField(required=False, allow_null=True)
    max_distance = serializers.CharField(required=False, allow_null=True)
