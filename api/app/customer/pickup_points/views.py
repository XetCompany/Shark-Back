from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.app.customer.pickup_points.serializers import PickupPointSerializer
from app.models import Cart, PointInCity, PointType


class PickupPointsView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses=PickupPointSerializer(many=True))
    def get(self, request):
        cart = Cart.objects.get_or_create(user=request.user)[0]

        # TODO: возможно убрать, если будет время
        first_cart_product = cart.products.first()
        company = first_cart_product.product.company if first_cart_product else None

        if not company:
            return Response([])

        pickup_points = PointInCity.objects.filter(company=company, type=PointType.PICKUP_POINT).all()

        serializer = PickupPointSerializer(pickup_points, many=True)
        return Response(serializer.data)
