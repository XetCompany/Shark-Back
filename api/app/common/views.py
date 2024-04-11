from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.app.common.serializers import UserInfoSerializer, CitySerializer, ProductCategorySerializer
from app.models import City, ProductCategory


@extend_schema(responses=UserInfoSerializer)
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def account_view(request):
    serializer = UserInfoSerializer(request.user)
    return Response(serializer.data)


@extend_schema(responses=CitySerializer(many=True))
@api_view(['GET'])
def cities_view(request):
    serializer = CitySerializer(City.objects.all(), many=True)
    return Response(serializer.data)


@extend_schema(responses=ProductCategorySerializer(many=True))
@api_view(['GET'])
def categories_view(request):
    serializer = ProductCategorySerializer(ProductCategory.objects.all(), many=True)
    return Response(serializer.data)
