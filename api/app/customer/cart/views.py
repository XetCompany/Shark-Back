from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.app.customer.cart.serializers import (
    CartProductSerializer, CartProductAddSerializer,
    CartProductUpdateSerializer,
)
from app.models import Cart, ProductCompany, Order


class CartView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses=CartProductSerializer(many=True))
    def get(self, request):
        cart = Cart.objects.get_or_create(user=request.user)[0]
        serializer = CartProductSerializer(cart.products, many=True)
        return Response(serializer.data)


class CartProductView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(request=CartProductAddSerializer, responses=CartProductAddSerializer)
    def post(self, request, product_id):
        product = ProductCompany.objects.get(id=product_id)
        cart = Cart.objects.get_or_create(user=request.user)[0]

        serializer = CartProductAddSerializer(data=request.data, context={'product': product, 'cart': cart})
        serializer.is_valid(raise_exception=True)
        cart_product = serializer.save()

        cart.products.add(cart_product)

        return Response(serializer.data)

    @extend_schema(request=CartProductUpdateSerializer, responses=204)
    def put(self, request, product_id):
        cart = Cart.objects.get(user=request.user)
        cart_product = cart.get_cart_product(product_id)
        serializer = CartProductUpdateSerializer(cart_product, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response()

    @extend_schema(responses=204)
    def delete(self, request, product_id):
        cart = Cart.objects.get(user=request.user)
        cart_product = cart.get_cart_product(product_id)
        cart.products.remove(cart_product)
        return Response()


class CartFromOrderView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses=204)
    def post(self, request, order_id):
        cart = Cart.objects.get_or_create(user=request.user)[0]
        if cart.products.exists():
            return Response({'error': 'Cart is not empty'}, status=400)

        order = Order.objects.get(id=order_id, user=request.user)
        cart.products.set([order_product.to_cart_product() for order_product in order.products.all()])

        return Response()
