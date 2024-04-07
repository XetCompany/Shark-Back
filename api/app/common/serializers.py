from django.contrib.auth.models import Group
from rest_framework import serializers

from app.models import User


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['groups'] = Group.objects.filter(user=instance).values_list('name', flat=True)
        return representation
