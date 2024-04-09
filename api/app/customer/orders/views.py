import logging

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.app.customer.orders.serializers import OrderSerializer, OrderEditSerializer
from app.models import Order, Cart, SearchInfo, OrderStatus, ProductInWarehouse


class OrderView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user).all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


class OrderSearchInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, search_info_id):
        """
        Создание заказа на основе информации о поиске маршрута и корзины
        """
        # TODO: проверка, на доступен ли продукт во время заказа, на складу и в корзине

        # Формирование заказа
        cart = Cart.objects.get_or_create(user=request.user)[0]
        if not cart.products.exists():
            return Response({'error': 'Cart is empty'}, status=400)

        search_info = SearchInfo.objects.get(id=search_info_id, user=request.user)
        groups_paths = [group_paths.get_copy() for group_paths in search_info.groups_paths.all()]
        order_products = []
        for cart_product in cart.products.all():
            order_products.append(cart_product.to_order_product())

        order = Order.objects.create(user=request.user)
        order.products.set(order_products)
        order.group_paths.set(groups_paths)
        # TODO: temp, мгновенная доставка, принимать должен Производитель или таймер
        order.status = OrderStatus.AWAITING
        order.save()

        # Очистка корзины
        cart.products.clear()

        # Очистка товаров на складах
        for group_paths in groups_paths:
            product_warehouse = ProductInWarehouse.objects.get(
                product=group_paths.product,
                warehouse=group_paths.warehouse
            )
            product_warehouse.count -= group_paths.count
            if product_warehouse.count == 0:
                product_warehouse.delete()
            elif product_warehouse.count < 0:
                logging.warning(f'Product {product_warehouse.product} in warehouse {product_warehouse.warehouse} has negative count: {product_warehouse.count}')
                product_warehouse.count = 0
                product_warehouse.save()
            else:
                product_warehouse.save()

        return Response(OrderSerializer(order).data)


class OrderInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        order = Order.objects.get(id=order_id, user=request.user)
        return Response(OrderSerializer(order).data)


class OrderStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):
        order = Order.objects.get(id=order_id, user=request.user)
        serializer = OrderEditSerializer(data=request.data, context={'order': order})
        serializer.is_valid(raise_exception=True)
        order.status = serializer.validated_data['status']
        order.decline_reason = serializer.validated_data.get('decline_reason')
        order.save()
        return Response(OrderSerializer(order).data)

