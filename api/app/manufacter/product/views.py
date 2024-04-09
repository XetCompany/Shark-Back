from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from app.models import ProductCompany
from .serializers import ProductSerializer


class ProductView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses=ProductSerializer(many=True))
    def get(self, request):
        products = ProductCompany.objects.filter(company=request.user).all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    @extend_schema(request=ProductSerializer, responses=ProductSerializer)
    def post(self, request):
        serializer = ProductSerializer(data=request.data, context={'company': request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ProductDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses=ProductSerializer)
    def get(self, request, product_id):
        product = ProductCompany.objects.get(id=product_id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    @extend_schema(request=ProductSerializer, responses=ProductSerializer)
    def put(self, request, product_id):
        product = ProductCompany.objects.get(id=product_id)
        serializer = ProductSerializer(data=request.data, instance=product, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @extend_schema(responses=204)
    def delete(self, request, product_id):
        product = ProductCompany.objects.get(id=product_id)
        product.delete()
        return Response(status=204)
