from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.app.customer.paths.serializers import PathsFiltersSerializer
from api.app.customer.paths.utils import search_paths
from api.app.customer.serializers import SearchInfoSerializer
from app.models import SearchInfo, PointInCity, PointType


class PickupPointPathsView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(parameters=[PathsFiltersSerializer], responses=SearchInfoSerializer(many=True))
    def get(self, request, pickup_point_id):
        serializer = PathsFiltersSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        # Очистка всех старых поисков
        search_infos = SearchInfo.objects.filter(user=request.user).all()
        for search_info in search_infos:
            for group_path in search_info.groups_paths.all():
                group_path.delete()

            search_info.delete()

        # Поиск всех путей
        # TODO: pickup_point небезопасно для company
        pickup_point = PointInCity.objects.get(id=pickup_point_id, type=PointType.PICKUP_POINT)
        search_paths(request.user, serializer.validated_data, pickup_point)

        # Получение поисковой информации
        search_infos = SearchInfo.objects.filter(user=request.user).all()
        serializer = SearchInfoSerializer(search_infos, many=True)

        return Response(serializer.data)


# TODO: проверка, на доступен ли продукт во время заказа
