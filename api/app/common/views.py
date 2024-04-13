from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.app.common.serializers import (
    UserInfoSerializer, CitySerializer, ProductCategorySerializer,
    UserInfoEditSerializer, NotificationSerializer,
)
from app.models import City, ProductCategory, Notification


class AccountView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses=UserInfoSerializer)
    def get(self, request):
        serializer = UserInfoSerializer(request.user)
        return Response(serializer.data)

    @extend_schema(request=UserInfoEditSerializer, responses=UserInfoEditSerializer)
    def put(self, request):
        serializer = UserInfoEditSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
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


class NotificationsView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses=NotificationSerializer(many=True))
    def get(self, request):
        notifications = Notification.objects.filter(user=request.user).all()[::-1]
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)


class ReadNotificationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        Notification.objects.filter(user=request.user).update(is_read=True)
        return Response()
