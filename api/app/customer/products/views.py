from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.app.common.serializers import ProductCompanySerializer
from api.app.customer.products.serializers import EvaluationAndCommentSerializer
from api.app.customer.products.utils import user_can_comment_product
from api.app.customer.serializers import ProductCompanyCustomerSerializer
from app.models import ProductCompany


class ProductsView(APIView):
    permission_classes = []

    def get(self, request):
        products = ProductCompany.objects.filter(is_available=True)
        serializer = ProductCompanyCustomerSerializer(products, many=True, context={'user': request.user})
        return Response(serializer.data)


class ProductInfoView(APIView):
    permission_classes = []

    def get(self, request, product_id):
        product = ProductCompany.objects.get(id=product_id)
        serializer = ProductCompanyCustomerSerializer(product, context={'user': request.user})
        return Response(serializer.data)


class ProductEvaluateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, product_id):
        product = ProductCompany.objects.get(id=product_id)
        serializer = EvaluationAndCommentSerializer(data=request.data, context={'user': request.user, 'product': product})
        serializer.is_valid(raise_exception=True)
        evaluation = serializer.save(author=request.user)
        product.evaluations.add(evaluation)
        return Response(serializer.data)
