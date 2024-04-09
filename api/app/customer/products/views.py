from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.app.common.serializers import ProductCompanySerializer
from api.app.customer.products.serializers import AddEvaluationAndCommentSerializer
from api.app.customer.serializers import ProductCompanyCustomerSerializer
from app.models import ProductCompany


class ProductsView(APIView):
    permission_classes = []

    @extend_schema(responses=ProductCompanySerializer(many=True))
    def get(self, request):
        products = ProductCompany.objects.filter(is_available=True)
        serializer = ProductCompanyCustomerSerializer(products, many=True, context={'user': request.user})
        return Response(serializer.data)


class ProductInfoView(APIView):
    permission_classes = []

    @extend_schema(responses=ProductCompanySerializer)
    def get(self, request, product_id):
        product = ProductCompany.objects.get(id=product_id)
        serializer = ProductCompanyCustomerSerializer(product, context={'user': request.user})
        return Response(serializer.data)


class ProductEvaluateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(request=AddEvaluationAndCommentSerializer, responses=AddEvaluationAndCommentSerializer)
    def post(self, request, product_id):
        product = ProductCompany.objects.get(id=product_id)
        serializer = AddEvaluationAndCommentSerializer(
            data=request.data,
            context={'user': request.user, 'product': product}
        )
        serializer.is_valid(raise_exception=True)
        evaluation = serializer.save(author=request.user)
        product.evaluations.add(evaluation)
        return Response(serializer.data)
