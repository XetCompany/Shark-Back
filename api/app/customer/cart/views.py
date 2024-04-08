from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.app.customer.cart.serializers import CartProductSerializer, CartProductAddSerializer
from app.models import Cart, ProductCompany


class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart = Cart.objects.get_or_create(user=request.user)[0]
        serializer = CartProductSerializer(cart.products, many=True)
        return Response(serializer.data)


class CartProductView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, product_id):
        product = ProductCompany.objects.get(id=product_id)

        serializer = CartProductAddSerializer(data=request.data, context={'product': product})
        serializer.is_valid(raise_exception=True)
        cart_product = serializer.save()

        cart = Cart.objects.get_or_create(user=request.user)[0]
        cart.products.add(cart_product)

        return Response(serializer.data)

    def put(self, request, product_id):
        cart = Cart.objects.get(user=request.user)
        cart_product = cart.get_cart_product(product_id)
        serializer = CartProductAddSerializer(cart_product, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response()

    def delete(self, request, product_id):
        cart = Cart.objects.get(user=request.user)
        cart_product = cart.get_cart_product(product_id)
        cart.products.remove(cart_product)
        return Response()
