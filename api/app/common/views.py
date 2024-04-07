from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.app.common.serializers import UserInfoSerializer


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def account_view(request):
    serializer = UserInfoSerializer(request.user)
    return Response(serializer.data)
