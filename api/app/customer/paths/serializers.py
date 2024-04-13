from rest_framework import serializers


class FloatOrNoneField(serializers.FloatField):
    def to_internal_value(self, data):
        data = None if data == 'null' else data
        return super().to_internal_value(data)


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

    min_price = FloatOrNoneField(min_value=0, required=False, allow_null=True)
    max_price = FloatOrNoneField(min_value=0, required=False, allow_null=True)
    min_time = FloatOrNoneField(min_value=0, required=False, allow_null=True)
    max_time = FloatOrNoneField(min_value=0, required=False, allow_null=True)
    min_distance = FloatOrNoneField(min_value=0, required=False, allow_null=True)
    max_distance = FloatOrNoneField(min_value=0, required=False, allow_null=True)

