from django.contrib.auth.models import Group
from rest_framework import serializers

from app.models import User, ProductCompany, EvaluationAndComment, City, ProductCategory


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'groups',)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['groups'] = Group.objects.filter(user=instance).values_list('name', flat=True)
        return representation


class EvaluationAndCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvaluationAndComment
        exclude = ('author',)


class ProductCompanySerializer(serializers.ModelSerializer):
    company = UserInfoSerializer()
    evaluations = EvaluationAndCommentSerializer(many=True)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['average_rating'] = instance.avg_evaluation
        return data

    class Meta:
        model = ProductCompany
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = '__all__'
