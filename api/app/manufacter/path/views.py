from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
    PathInfoSerializer, PathEditSerializer,
    PathCreateSerializer, ImportExcelSerializer,
)
from .utils import import_from_excel, get_pattern_excel


class PathView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses=PathInfoSerializer(many=True))
    def get(self, request):
        paths = request.user.paths.all()
        serializer = PathInfoSerializer(paths, many=True)
        return Response(serializer.data)

    @extend_schema(request=PathCreateSerializer, responses=PathCreateSerializer)
    def post(self, request):
        user = request.user
        serializer = PathCreateSerializer(data=request.data, context={'user': user})
        serializer.is_valid(raise_exception=True)
        path = serializer.save()
        user.paths.add(path)
        return Response(serializer.data)


class PathExcelView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Получение шаблона для загрузки путей
        """
        return get_pattern_excel()

    @extend_schema(request=ImportExcelSerializer)
    def post(self, request):
        """
        Загрузка путей из excel
        Должен использоваться файл в формате xlsx
        """
        serializer = ImportExcelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        excel = serializer.validated_data['excel']
        import_from_excel(excel, request.user)
        return Response()


class PathDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses=PathInfoSerializer)
    def get(self, request, path_id):
        path = request.user.paths.get(id=path_id)
        serializer = PathInfoSerializer(path)
        return Response(serializer.data)

    @extend_schema(request=PathEditSerializer, responses=PathEditSerializer)
    def put(self, request, path_id):
        path = request.user.paths.get(id=path_id)
        serializer = PathEditSerializer(data=request.data, instance=path, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @extend_schema(responses={204: None})
    def delete(self, request, path_id):
        path = request.user.paths.get(id=path_id)
        path.delete()
        return Response(status=204)
