from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from api.auth.reset_password.utils import generate_reset_token, send_email_reset_password
from utils.data import get_data_value


@api_view(['POST'])
@permission_classes([AllowAny])
def request_password_reset_email(request):
    email = get_data_value(request, 'email')
    token = generate_reset_token(email)
    send_email_reset_password(email, token.user.username, token.token)

    # TODO: удалить после тестирования
    return Response({'token': token.token})


