from django.contrib.auth.models import Group
from rest_framework import serializers

from app.models import User, ProductCompany


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'groups',)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['groups'] = Group.objects.filter(user=instance).values_list('name', flat=True)
        return representation


class ProductCompanySerializer(serializers.ModelSerializer):
    company = UserInfoSerializer()

    class Meta:
        model = ProductCompany
        fields = '__all__'
