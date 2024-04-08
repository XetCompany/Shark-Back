from rest_framework.response import Response
from rest_framework.views import APIView

from api.app.common.serializers import ProductCompanySerializer
from app.models import ProductCompany


class ProductsView(APIView):
    permission_classes = []

    def get(self, request):
        products = ProductCompany.objects.filter(is_available=True)
        serializer = ProductCompanySerializer(products, many=True)
        return Response(serializer.data)
