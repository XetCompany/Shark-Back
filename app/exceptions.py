from rest_framework.exceptions import APIException


class ParameterIsMissing(APIException):
    status_code = 400
    default_detail = 'Parameter "{param}" is missing'
    default_code = 'parameter_is_missing'

    def __init__(self, param: str):
        self.param = param
        super().__init__(self.default_detail.format(param=param))


class UserDoesNotExist(APIException):
    status_code = 400
    default_detail = 'User with email "{email}" does not exist'
    default_code = 'user_does_not_exist'

    def __init__(self, email: str):
        self.email = email
        super().__init__(self.default_detail.format(email=email))


class TokenValidationFailed(APIException):
    status_code = 400
    default_detail = 'Token validation failed'
    default_code = 'token_validation_failed'

    def __init__(self):
        super().__init__(self.default_detail)
