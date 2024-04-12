from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password as django_validate_password
from rest_framework import serializers

from api.auth.register.validators import NotEmailValidator


UserModel = get_user_model()

roles = [
    ("manufacturer", "manufacturer"),
    ("customer", "customer"),
]


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255, validators=[NotEmailValidator()])
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=255, write_only=True)

    role = serializers.ChoiceField(choices=roles)

    class Meta:
        model = UserModel
        fields = ('username', 'email', 'password', 'role')

    def validate_username(self, value):
        if self.Meta.model.objects.filter(username=value).exists():
            raise serializers.ValidationError('Пользователь с таким логином уже существует')
        return value

    def validate_email(self, value):
        if self.Meta.model.objects.filter(email=value).exists():
            raise serializers.ValidationError('Пользователь с таким e-mail уже существует')
        return value

    def validate_password(self, value):
        django_validate_password(value)
        return value

    # def validate_role(self, value):
    #     if value not in ['customer', 'performer']:
    #         raise serializers.ValidationError('Неверный тип пользователя')
    #     return value

    def create(self, validated_data):
        role = validated_data.pop('role')
        user = UserModel.objects.create_user(**validated_data)
        user.add_group(role)

        return user


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=255)
    new_password = serializers.CharField(max_length=255)

    def validate_old_password(self, value):
        if not self.context['request'].user.check_password(value):
            raise serializers.ValidationError('Неверный пароль')
        return value

    def validate_new_password(self, value):
        django_validate_password(value)
        return value

    def validate(self, attrs):
        if attrs['old_password'] == attrs['new_password']:
            raise serializers.ValidationError('Новый пароль не должен совпадать со старым')
        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        user.set_password(validated_data['new_password'])
        user.save()
        return user
