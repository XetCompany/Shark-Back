import logging

from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.app.customer.orders.serializers import OrderSerializer, OrderEditSerializer
from api.app.customer.products.utils import user_can_comment_product
from app.models import Order, Cart, SearchInfo, OrderStatus, ProductInWarehouse, Notification, NotificationType


class OrderView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses=OrderSerializer(many=True))
    def get(self, request):
        orders = Order.objects.filter(user=request.user).all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


class OrderSearchInfoView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses=OrderSerializer)
    def post(self, request, search_info_id):
        """
        Создание заказа на основе информации о поиске маршрута и корзины
        """
        # TODO: проверка, на доступен ли продукт во время заказа, на складу и в корзине
        products_can_comments = []
        for cart_product in Cart.objects.get_or_create(user=request.user)[0].products.all():
            products_can_comments.append((cart_product.product, user_can_comment_product(request.user, cart_product.product)))

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

        if not order_products:
            return Response({'error': 'No products in order'}, status=400)

        # Отправка уведомления производителю
        company = order_products[0].product.company
        Notification.objects.create(
            user=company,
            text=f'Пользователь {request.user.username} оформил заказ на ваш(и) продукт(ы)',
            type=NotificationType.TYPE_ORDER,
            additional_data={'order_id': order.id},
        )

        # Отправка уведомления покупателю
        Notification.objects.create(
            user=request.user,
            text=f'Ваш заказ на продукт(ы) {", ".join([product.product.name for product in order_products])} успешно доставлен',
            type=NotificationType.TYPE_DELIVERED,
            additional_data={'order_id': order.id},
        )

        # Никогда не сработает???
        for product, can_comment in products_can_comments:
            if can_comment:
                continue
            now_can_comment = user_can_comment_product(request.user, product)
            if now_can_comment:
                Notification.objects.create(
                    user=request.user,
                    text=f'Теперь вы можете оставить отзыв на продукт {product.name}',
                    type=NotificationType.TYPE_CAN_COMMENT,
                    additional_data={'product_id': product.id},
                )

        return Response(OrderSerializer(order).data)


class OrderInfoView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses=OrderSerializer)
    def get(self, request, order_id):
        order = Order.objects.get(id=order_id, user=request.user)
        return Response(OrderSerializer(order).data)


class OrderStatusView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(request=OrderEditSerializer, responses=OrderSerializer)
    def post(self, request, order_id):
        order = Order.objects.get(id=order_id, user=request.user)

        products_can_comments = []
        for order_product in order.products.all():
            products_can_comments.append((order_product.product, user_can_comment_product(request.user, order_product.product)))

        serializer = OrderEditSerializer(data=request.data, context={'order': order})
        serializer.is_valid(raise_exception=True)
        order.status = serializer.validated_data['status']
        order.decline_reason = serializer.validated_data.get('decline_reason')
        order.save()

        for product, can_comment in products_can_comments:
            if can_comment:
                continue
            now_can_comment = user_can_comment_product(request.user, product)
            if now_can_comment:
                Notification.objects.create(
                    user=request.user,
                    text=f'Теперь вы можете оставить отзыв на продукт {product.name}',
                    type=NotificationType.TYPE_CAN_COMMENT,
                    additional_data={'product_id': product.id},
                )

        return Response(OrderSerializer(order).data)

