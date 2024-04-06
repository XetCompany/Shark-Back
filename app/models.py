from datetime import timedelta, datetime

from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    username = models.CharField(
        verbose_name='Логин',
        max_length=255,
        unique=True
    )
    email = models.EmailField(
        verbose_name='E-mail',
        max_length=255,
        unique=True
    )
    fullname = models.CharField(
        verbose_name='ФИО',
        max_length=255,
        blank=True,
        null=True
    )
    phone = PhoneNumberField(
        verbose_name='Телефон',
        blank=True,
        null=True,
        default=None
    )
    description = models.TextField(
        verbose_name='Описание',
        max_length=255,
        blank=True,
        null=True
    )

    def add_group(self, group_name):
        group = Group.objects.get(name=group_name)
        self.groups.add(group)

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'id: {self.id}, login: {self.username}'


class ResetPasswordToken(models.Model):
    user = models.ForeignKey(
        verbose_name='Пользователь', to='User',
        on_delete=models.CASCADE
    )
    token = models.CharField(verbose_name='Токен', unique=True, max_length=255)
    created_at = models.DateTimeField(
        verbose_name='Время создания',
        auto_now_add=True
    )

    # TODO: сделать удаление токена через 1 час

    def is_expired(self):
        future_time = self.created_at + timedelta(hours=1)
        now_time = datetime.now(tz=None) - timedelta(hours=3)
        # TODO: костыль
        now_time = now_time.replace(tzinfo=None)
        future_time = future_time.replace(tzinfo=None)
        return now_time > future_time

    def is_valid(self):
        return not self.is_expired()

    class Meta:
        ordering = ('id',)
        verbose_name = 'Токен для сброса пароля'
        verbose_name_plural = 'Токены для сброса пароля'

    def __str__(self):
        return f'id: {self.id}, user: {self.user.username}'
