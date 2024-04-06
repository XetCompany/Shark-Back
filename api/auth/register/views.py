from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import RegisterSerializer


@api_view(['POST'])
def register_handler(request):
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response()
