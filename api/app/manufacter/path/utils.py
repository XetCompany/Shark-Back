import io
from decimal import Decimal

import pandas as pd
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import Q
from django.http import FileResponse
from rest_framework.exceptions import APIException

from app.models import City, Path, converter_path_type


def get_city(name: str):
    try:
        city = City.objects.get(name=name)
    except City.DoesNotExist:
        raise APIException(f'City {name} does not exist')

    return city


def get_pattern_excel():
    headers = [
        'Точка А',
        'Точка Б',
        'Время (в часах)',
        'Цена (в рублях)',
        'Протяженность (в км)',
        'Тип прохождения (Автомобильный, Железнодорожный, Морской, Речной, Воздушный)',
    ]
    df = pd.DataFrame(columns=headers)
    buffer = io.BytesIO()
    df.to_excel(buffer, index=False)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='pattern.xlsx')


def import_from_excel(excel: InMemoryUploadedFile, user):
    try:
        df = pd.read_excel(excel)
    except Exception:
        raise APIException('Invalid file format')

    for row in df.itertuples():
        try:
            _, point_a, point_b, time, price, length, type_path = row
        except ValueError:
            raise APIException('Invalid table format')

        city_a = get_city(point_a)
        city_b = get_city(point_b)
        time = int(time)
        price = Decimal(price)
        length = Decimal(length)
        if type_path not in converter_path_type:
            raise APIException(f'Invalid path type {type_path}')
        type_path = converter_path_type[type_path]

        if city_a == city_b:
            raise APIException('Points must be different')

        existed_path = user.paths.filter(
            Q(point_a=city_a, point_b=city_b, type=type_path) |
            Q(point_a=city_b, point_b=city_a, type=type_path)
        ).first()
        if existed_path:
            existed_path.time = time
            existed_path.price = price
            existed_path.length = length
            existed_path.save()
            continue

        path = Path.objects.create(
            point_a=city_a, point_b=city_b, time=time, price=price, length=length, type=type_path
        )
        user.paths.add(path)
