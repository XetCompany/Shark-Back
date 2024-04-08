from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
    PathInfoSerializer, PathSerializer,
    PathCreateSerializer,
)


class PathView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        paths = request.user.paths.all()
        serializer = PathInfoSerializer(paths, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PathCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        path = serializer.save()
        user = request.user
        user.paths.add(path)
        return Response(serializer.data)


class PathDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, path_id):
        path = request.user.paths.get(id=path_id)
        serializer = PathInfoSerializer(path)
        return Response(serializer.data)

    def put(self, request, path_id):
        path = request.user.paths.get(id=path_id)
        serializer = PathSerializer(data=request.data, instance=path, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, path_id):
        path = request.user.paths.get(id=path_id)
        path.delete()
        return Response(status=204)
