from django.contrib.auth.models import Group
from rest_framework import serializers

from api.app.common.fields import ImageBase64Field
from app.models import User, ProductCompany, EvaluationAndComment, City, ProductCategory


class UserInfoSerializer(serializers.ModelSerializer):
    image = ImageBase64Field(required=False, base64_type='image')

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'fullname', 'phone', 'description', 'image', 'groups',)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['groups'] = Group.objects.filter(user=instance).values_list('name', flat=True)
        return representation


class UserInfoEditSerializer(serializers.ModelSerializer):
    image = ImageBase64Field(required=False, base64_type='image', allow_null=True)

    class Meta:
        model = User
        fields = ('username', 'fullname', 'phone', 'description', 'image')


class EvaluationAndCommentSerializer(serializers.ModelSerializer):
    author = UserInfoSerializer()

    class Meta:
        model = EvaluationAndComment
        fields = '__all__'


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
