from rest_framework import serializers

from api.app.common.fields import ImageBase64Field
from api.app.common.serializers import EvaluationAndCommentSerializer
from app.models import ProductCompany


class ProductSerializer(serializers.ModelSerializer):
    photo = ImageBase64Field(required=False, base64_type='image', allow_null=True)
    evaluations = EvaluationAndCommentSerializer(many=True, read_only=True)

    class Meta:
        model = ProductCompany
        exclude = ('company',)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['average_rating'] = instance.avg_evaluation
        return data

    def create(self, validated_data):
        company = self.context['company']
        return super().create({**validated_data, 'company': company})
