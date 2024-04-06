import secrets

from django.contrib.auth import get_user_model

from app.exceptions import UserDoesNotExist, TokenValidationFailed
from app.models import ResetPasswordToken

UserModel = get_user_model()


def get_user(email):
    try:
        return UserModel.objects.get(email=email)
    except UserModel.DoesNotExist:
        raise UserDoesNotExist(email)


def generate_reset_token(email) -> ResetPasswordToken:
    user = get_user(email)
    token_str = secrets.token_urlsafe(64)
    token = ResetPasswordToken.objects.create(user=user, token=token_str)
    return token


def get_token(token_str):
    try:
        return ResetPasswordToken.objects.get(token=token_str)
    except ResetPasswordToken.DoesNotExist:
        raise TokenValidationFailed()


def check_token(token: ResetPasswordToken, raise_exception=True):
    is_valid = token.is_valid()
    if not is_valid and raise_exception:
        raise TokenValidationFailed()
    return is_valid


def reset_password_token(token, password):
    token.user.set_password(password)
    token.user.save()
    token.delete()
