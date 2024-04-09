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

    min_price = serializers.FloatField(min_value=0, required=False)
    max_price = serializers.FloatField(min_value=0, required=False)
    min_time = serializers.FloatField(min_value=0, required=False)
    max_time = serializers.FloatField(min_value=0, required=False)
    min_distance = serializers.FloatField(min_value=0, required=False)
    max_distance = serializers.FloatField(min_value=0, required=False)

