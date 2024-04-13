from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.app.customer.orders.serializers import OrderSerializer
from app.models import Order


class OrderView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses=OrderSerializer(many=True))
    def get(self, request):
        orders = Order.objects.filter(products__product__company=request.user).all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
