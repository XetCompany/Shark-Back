import base64

from django.core.files.base import ContentFile
from rest_framework import serializers


class FileBase64Field(serializers.ImageField):
    def __init__(self, *, base64_type="", **kwargs):
        self.base64_type = base64_type
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        file_data = data['data']
        filename = data['name']
        data_file = None
        if file_data.startswith(f'data:{self.base64_type}'):
            format, filestr = file_data.split(';base64,')
            data_file = ContentFile(base64.b64decode(filestr), name=filename)
        return super().to_internal_value(data_file)
