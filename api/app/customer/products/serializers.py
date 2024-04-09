from rest_framework import serializers

from api.app.customer.products.utils import user_can_comment_product
from app.models import EvaluationAndComment


class EvaluationAndCommentSerializer(serializers.ModelSerializer):
    evaluation = serializers.IntegerField(min_value=1, max_value=5)

    class Meta:
        model = EvaluationAndComment
        exclude = ('author',)

    def validate(self, attrs):
        user = self.context['user']
        product = self.context['product']
        if not user_can_comment_product(user, product):
            raise serializers.ValidationError('You cannot comment this product')
        return attrs
