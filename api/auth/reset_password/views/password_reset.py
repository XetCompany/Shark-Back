from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth.password_validation import validate_password as django_validate_password

from api.auth.reset_password.utils import get_token, check_token, reset_password_token
from utils.data import get_data_value


@permission_classes([AllowAny])
@api_view(['POST'])
def password_reset_email(request):
    token_str = get_data_value(request, 'token')
    password = get_data_value(request, 'password')

    token = get_token(token_str)
    check_token(token)
    django_validate_password(password)
    reset_password_token(token, password)

    return Response({'message': 'Пароль успешно изменен'})
