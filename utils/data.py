from app.exceptions import ParameterIsMissing


def get_data_value(request, key):
    value = request.data.get(key, None)
    if value is None:
        raise ParameterIsMissing(key)
    return value
