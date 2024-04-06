from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

UserModel = get_user_model()


class CustomModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        if username is None or password is None:
            return
        try:
            user_email = UserModel._default_manager.filter(email=username)
            user_username = UserModel._default_manager.filter(username=username)

            if all([user_email.exists(), user_username.exists()]):
                return

            if user_email.exists():
                user = user_email[0]
            elif user_username.exists():
                user = user_username[0]
            else:
                raise UserModel.DoesNotExist

        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user