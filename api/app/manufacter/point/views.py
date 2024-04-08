from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from app.models import PointInCity
from .serializers import (
    PointInCitySerializer
)


class PointView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        points = request.user.points.all()
        serializer = PointInCitySerializer(points, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PointInCitySerializer(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class PointDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, point_id):
        point = PointInCity.objects.get(id=point_id, company=request.user)
        serializer = PointInCitySerializer(point)
        return Response(serializer.data)

    def delete(self, request, point_id):
        point = PointInCity.objects.get(id=point_id, company=request.user)
        point.delete()
        return Response(status=204)
