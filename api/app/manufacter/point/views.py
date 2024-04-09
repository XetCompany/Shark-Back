from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from app.models import PointInCity, ProductInWarehouse, ProductCompany
from .serializers import (
    PointInCitySerializer, ProductInWarehouseDetailSerializer,
    ProductInWarehouseSerializer,
)


class PointView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses=PointInCitySerializer(many=True))
    def get(self, request):
        points = PointInCity.objects.filter(company=request.user)
        serializer = PointInCitySerializer(points, many=True)
        return Response(serializer.data)

    @extend_schema(request=PointInCitySerializer, responses=PointInCitySerializer)
    def post(self, request):
        serializer = PointInCitySerializer(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class PointDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses=PointInCitySerializer)
    def get(self, request, point_id):
        point = PointInCity.objects.get(id=point_id, company=request.user)
        serializer = PointInCitySerializer(point)
        return Response(serializer.data)

    @extend_schema(responses=204)
    def delete(self, request, point_id):
        point = PointInCity.objects.get(id=point_id, company=request.user)
        point.delete()
        return Response(status=204)


class PointProductView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses=ProductInWarehouseDetailSerializer(many=True))
    def get(self, request, point_id):
        point = PointInCity.objects.get(id=point_id, company=request.user)
        products = ProductInWarehouse.objects.filter(warehouse=point)
        serializer = ProductInWarehouseDetailSerializer(products, many=True)
        return Response(serializer.data)


class PointProductDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses=ProductInWarehouseDetailSerializer)
    def get(self, request, point_id, product_id):
        product = ProductInWarehouse.objects.get(
            id=product_id, warehouse__point__id=point_id, warehouse__point__company=request.user
        )
        serializer = ProductInWarehouseDetailSerializer(product)
        return Response(serializer.data)

    @extend_schema(request=ProductInWarehouseSerializer, responses=ProductInWarehouseDetailSerializer)
    def put(self, request, point_id, product_id):
        product = ProductInWarehouse.objects.get(
            id=product_id, warehouse__point__id=point_id, warehouse__point__company=request.user
        )
        serializer = ProductInWarehouseSerializer(data=request.data, instance=product, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @extend_schema(responses=ProductInWarehouseSerializer)
    def post(self, request, point_id, product_id):
        product = ProductCompany.objects.get(id=product_id, company=request.user)
        point = PointInCity.objects.get(id=point_id, company=request.user)
        serializer = ProductInWarehouseSerializer(data=request.data, context={'warehouse': point, 'product': product})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @extend_schema(responses=204)
    def delete(self, request, point_id, product_id):
        product = ProductInWarehouse.objects.get(
            id=product_id, warehouse__point__id=point_id, warehouse__point__company=request.user
        )
        product.delete()
        return Response(status=204)
