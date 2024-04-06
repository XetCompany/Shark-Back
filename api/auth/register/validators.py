from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.validators import EmailValidator
from rest_framework.exceptions import ValidationError as DRFValidationError


class NotEmailValidator(EmailValidator):
    def __call__(self, value):
        try:
            super().__call__(value)
        except (DRFValidationError, DjangoValidationError):
            return value
        raise DRFValidationError('Поле не может быть e-mail адресом')
