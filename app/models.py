from datetime import timedelta, datetime

from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class ProductCategory(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=255,
        unique=True
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Категория товара'
        verbose_name_plural = 'Категории товаров'

    def __str__(self):
        return f'id: {self.id}, name: {self.name}'


class ProductCompany(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=255,
        unique=True
    )
    photo = models.ImageField(
        verbose_name='Фото',
        upload_to='product_companies/',
        blank=True,
        null=True
    )
    price = models.DecimalField(
        verbose_name='Цена',
        max_digits=10,
        decimal_places=2,
        default=0
    )
    sizes = models.CharField(
        verbose_name='Размеры',
        max_length=255,
        blank=True,
        null=True
    )
    weight = models.DecimalField(
        verbose_name='Масса',
        max_digits=10,
        decimal_places=2,
        default=0
    )
    description = models.TextField(
        verbose_name='Описание',
        max_length=255,
        blank=True,
        null=True
    )
    category = models.ForeignKey(
        verbose_name='Категория',
        to='ProductCategory',
        on_delete=models.CASCADE
    )
    is_available = models.BooleanField(
        verbose_name='Доступность для покупателя',
        default=True
    )
    company = models.ForeignKey(
        verbose_name='Компания производитель',
        to='User',
        on_delete=models.CASCADE
    )


class City(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=255,
        unique=True
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

    def __str__(self):
        return f'id: {self.id}, name: {self.name}'


class PointType(models.TextChoices):
    WAREHOUSE = 'warehouse', 'Склад'
    PICKUP_POINT = 'pickup_point', 'Пункт выдачи'


class PointInCity(models.Model):
    city = models.ForeignKey(
        verbose_name='Город',
        to='City',
        on_delete=models.CASCADE
    )
    type = models.CharField(
        verbose_name='Тип',
        max_length=255,
        choices=PointType.choices
    )
    company = models.ForeignKey(
        verbose_name='Компания',
        to='User',
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Точка в городе'
        verbose_name_plural = 'Точки в городах'
        unique_together = ('city', 'type', 'company')

    def __str__(self):
        return f'id: {self.id}, city: {self.city.name}, type: {self.type}, company: {self.company.username}'


class ProductInWarehouse(models.Model):
    product = models.ForeignKey(
        verbose_name='Изделие производства',
        to='ProductCompany',
        on_delete=models.CASCADE
    )
    warehouse = models.ForeignKey(
        verbose_name='Склад',
        to='PointInCity',
        on_delete=models.CASCADE
    )
    count = models.PositiveIntegerField(
        verbose_name='Количество'
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Изделие на складе'
        verbose_name_plural = 'Изделия на складах'

    def __str__(self):
        return f'id: {self.id}, product: {self.product.name}, warehouse: {self.warehouse.city.name}'


class PathType(models.TextChoices):
    AUTOMOBILE = 'automobile', 'Автомобильный'
    RAILWAY = 'railway', 'Железнодорожный'
    SEA = 'sea', 'Морской'
    RIVER = 'river', 'Речной'
    AIR = 'air', 'Воздушный'


class Path(models.Model):
    point_a = models.ForeignKey(
        verbose_name='Точка А',
        to='City',
        on_delete=models.CASCADE,
        related_name='point_a'
    )
    point_b = models.ForeignKey(
        verbose_name='Точка Б',
        to='City',
        on_delete=models.CASCADE,
        related_name='point_b'
    )
    time = models.PositiveIntegerField(
        verbose_name='Время прохождения(В часах)'
    )
    price = models.DecimalField(
        verbose_name='Цена прохождения(В рублях)',
        max_digits=10,
        decimal_places=2,
        default=0
    )
    length = models.DecimalField(
        verbose_name='Протяженность(В километрах)',
        max_digits=10,
        decimal_places=2,
        default=0
    )
    type = models.CharField(
        verbose_name='Тип прохождения',
        max_length=255,
        choices=PathType.choices,
        default=PathType.AUTOMOBILE
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Путь'
        verbose_name_plural = 'Пути'

    def __str__(self):
        return f'id: {self.id}, point_a: {self.point_a.city.name}, point_b: {self.point_b.city.name}'


class PathGroup(models.Model):
    path = models.ForeignKey(
        verbose_name='Путь',
        to='Path',
        on_delete=models.CASCADE
    )
    group = models.ForeignKey(
        verbose_name='Группа путей',
        to='GroupPaths',
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Путь заказа'
        verbose_name_plural = 'Пути заказа'

    def __str__(self):
        return f'id: {self.id}'


class GroupPaths(models.Model):
    paths = models.ManyToManyField(
        verbose_name='Пути',
        to='Path',
        through='PathGroup',
    )

    product = models.ForeignKey(
        verbose_name='Изделие производства',
        to='ProductCompany',
        on_delete=models.CASCADE
    )
    count = models.PositiveIntegerField(
        verbose_name='Количество'
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Группа путей заказа'
        verbose_name_plural = 'Группы путей заказа'

    def __str__(self):
        return f'id: {self.id}'


class SearchInfo(models.Model):
    user = models.ForeignKey(
        verbose_name='Пользователь',
        to='User',
        on_delete=models.CASCADE
    )
    group_paths = models.ForeignKey(
        verbose_name='Группа путей',
        to='GroupPaths',
        on_delete=models.CASCADE
    )


class OrderProduct(models.Model):
    product = models.ForeignKey(
        verbose_name='Изделие производства',
        to='ProductCompany',
        on_delete=models.CASCADE
    )
    count = models.PositiveIntegerField(
        verbose_name='Количество'
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Заказной продукт'
        verbose_name_plural = 'Заказные продукты'

    def __str__(self):
        return f'id: {self.id}, product: {self.product.name}'


class OrderStatus(models.TextChoices):
    """
    Статус заказа
    new - заказ просто создан, пока что просто заполняется продуктами
    in_progress - заказ находится в доставке, доставка выбрана, заказ отправлен
    awaiting - заказ ожидает забора, покупатель примет или отклонит заказ
    delivered - заказ доставлен
    """
    NEW = 'new', 'Новый'
    IN_PROGRESS = 'in_progress', 'В процессе'
    AWAITING = 'awaiting', 'Ожидает забора'
    DELIVERED = 'delivered', 'Доставлен'


class Order(models.Model):
    products = models.ManyToManyField(
        verbose_name='Заказные продукты',
        to='OrderProduct'
    )
    group_paths = models.ManyToManyField(
        verbose_name='Группы путей',
        to='GroupPaths',
    )
    status = models.CharField(
        verbose_name='Статус',
        max_length=255,
        choices=OrderStatus.choices,
        default=OrderStatus.NEW
    )
    decline_reason = models.TextField(
        verbose_name='Причина отклонения',
        blank=True,
        null=True
    )
    user = models.ForeignKey(
        verbose_name='Пользователь',
        to='User',
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'id: {self.id}'


class CartProduct(models.Model):
    product = models.ForeignKey(
        verbose_name='Изделие производства',
        to='ProductCompany',
        on_delete=models.CASCADE
    )
    count = models.PositiveIntegerField(
        verbose_name='Количество'
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'

    def __str__(self):
        return f'id: {self.id}, product: {self.product.name}'


class Cart(models.Model):
    products = models.ManyToManyField(
        verbose_name='Товары',
        to='CartProduct'
    )
    user = models.ForeignKey(
        verbose_name='Пользователь',
        to='User',
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        return f'id: {self.id}'


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

    paths = models.ManyToManyField(
        verbose_name='Пути',
        to='Path',
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
