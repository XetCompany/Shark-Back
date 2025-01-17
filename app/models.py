from datetime import timedelta, datetime

from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone


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
    # TODO: убрать уникальность для названия
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
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    # TODO: сделать проверки на доступность
    is_available = models.BooleanField(
        verbose_name='Доступность для покупателя',
        default=True
    )
    company = models.ForeignKey(
        verbose_name='Компания производитель',
        to='User',
        on_delete=models.CASCADE
    )
    evaluations = models.ManyToManyField(
        verbose_name='Оценки и комментарии',
        to='EvaluationAndComment',
        blank=True
    )

    @property
    def avg_evaluation(self):
        evaluations = self.evaluations.all()
        if not evaluations:
            return 0
        return sum([evaluation.evaluation for evaluation in evaluations]) / len(evaluations)

    @property
    def warehouses(self):
        p_w = ProductInWarehouse.objects.filter(product=self)
        return [product_warehouse.warehouse for product_warehouse in p_w]

    class Meta:
        ordering = ('id',)
        verbose_name = 'Изделие производства'
        verbose_name_plural = 'Изделия производства'

    def __str__(self):
        return f'id: {self.id}, name: {self.name}'


class EvaluationAndComment(models.Model):
    evaluation = models.PositiveIntegerField(
        verbose_name='Оценка'
    )
    comment = models.TextField(
        verbose_name='Комментарий',
        blank=True,
        null=True
    )
    author = models.ForeignKey(
        verbose_name='Автор',
        to='User',
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Оценка и комментарий'
        verbose_name_plural = 'Оценки и комментарии'

    def __str__(self):
        return f'id: {self.id}, evaluation: {self.evaluation}, comment: {self.comment}'


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
    name = models.CharField(
        verbose_name='Название',
        max_length=255
    )
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

    @classmethod
    def get_warehouse_by_city_name(cls, city_name, company):
        return cls.objects.get(city__name=city_name, type=PointType.WAREHOUSE, company=company)

    class Meta:
        ordering = ('id',)
        verbose_name = 'Точка в городе'
        verbose_name_plural = 'Точки в городах'
        unique_together = ('city', 'type', 'company')

    def __str__(self):
        return f'id: {self.id}, name: {self.name}, city: {self.city.name}, type: {self.type}, company: {self.company.username}'


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
        return f'id: {self.id}, product: {self.product.name}, warehouse: {self.warehouse.city.name} count: {self.count}'


class PathType(models.TextChoices):
    AUTOMOBILE = 'automobile', 'Автомобильный'
    RAILWAY = 'railway', 'Железнодорожный'
    SEA = 'sea', 'Морской'
    RIVER = 'river', 'Речной'
    AIR = 'air', 'Воздушный'
    INSTANT = 'instant', 'Мгновенный'


converter_path_type = {
    'Автомобильный': PathType.AUTOMOBILE,
    'Железнодорожный': PathType.RAILWAY,
    'Морской': PathType.SEA,
    'Речной': PathType.RIVER,
    'Воздушный': PathType.AIR
}


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
        return f'id: {self.id}, point_a: {self.point_a.name}, point_b: {self.point_b.name} type: {self.type}'


class GroupPath(models.Model):
    path = models.ForeignKey(
        verbose_name='Путь',
        to='Path',
        on_delete=models.CASCADE
    )
    is_reversed = models.BooleanField(
        verbose_name='Обратный путь',
        default=False
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Путь заказа'
        verbose_name_plural = 'Пути заказа'

    def __str__(self):
        return f'id: {self.id}, path: {self.path.point_a.name} -> {self.path.point_b.name} is_reversed: {self.is_reversed}'


class GroupPathsRelation(models.Model):
    group_paths = models.ForeignKey(
        verbose_name='Группа путей',
        to='GroupPaths',
        on_delete=models.CASCADE
    )
    group_path = models.ForeignKey(
        verbose_name='Путь заказа',
        to='GroupPath',
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Связь группы путей и пути заказа'
        verbose_name_plural = 'Связи группы путей и пути заказа'

    def __str__(self):
        return f'id: {self.id} group_paths: {self.group_paths.id} group_path: {self.group_path.id}'


class GroupPaths(models.Model):
    paths = models.ManyToManyField(
        verbose_name='Пути',
        to='GroupPath',
        through='GroupPathsRelation'
    )
    is_instant_delivery = models.BooleanField(
        verbose_name='Мгновенная доставка',
        default=False
    )
    instant_city = models.ForeignKey(
        verbose_name='Город мгновенной доставки',
        to='City',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        default=None
    )
    product = models.ForeignKey(
        verbose_name='Изделие производства',
        to='ProductCompany',
        on_delete=models.CASCADE
    )
    count = models.PositiveIntegerField(
        verbose_name='Количество'
    )
    warehouse = models.ForeignKey(
        verbose_name='Склад',
        to='PointInCity',
        on_delete=models.CASCADE
    )

    def get_copy(self):
        group_paths = GroupPaths.objects.create(product=self.product, count=self.count, warehouse=self.warehouse, is_instant_delivery=self.is_instant_delivery, instant_city=self.instant_city)
        for group_path in self.paths.all():
            GroupPathsRelation.objects.create(group_paths=group_paths, group_path=group_path)
        return group_paths

    class Meta:
        ordering = ('id',)
        verbose_name = 'Группа путей заказа'
        verbose_name_plural = 'Группы путей заказа'

    def __str__(self):
        return f'id: {self.id} product: {self.product.name} count: {self.count} warehouse: {self.warehouse.city.name}'


class SearchInfo(models.Model):
    user = models.ForeignKey(
        verbose_name='Пользователь',
        to='User',
        on_delete=models.CASCADE
    )
    groups_paths = models.ManyToManyField(
        verbose_name='Группы путей',
        to='GroupPaths'
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Информация о поиске'
        verbose_name_plural = 'Информации о поиске'

    def __str__(self):
        return f'id: {self.id}'


class OrderProduct(models.Model):
    product = models.ForeignKey(
        verbose_name='Изделие производства',
        to='ProductCompany',
        on_delete=models.CASCADE
    )
    count = models.PositiveIntegerField(
        verbose_name='Количество'
    )

    def to_cart_product(self):
        return CartProduct.objects.create(product=self.product, count=self.count)

    class Meta:
        ordering = ('id',)
        verbose_name = 'Заказной продукт'
        verbose_name_plural = 'Заказные продукты'

    def __str__(self):
        return f'id: {self.id}, product: {self.product.name}'


class OrderStatus(models.TextChoices):
    """
    Статус заказа
    in_progress - заказ находится в доставке, доставка выбрана, заказ отправлен
    awaiting - заказ ожидает забора, покупатель примет или отклонит заказ
    delivered - заказ доставлен
    """
    IN_PROGRESS = 'in_progress', 'В процессе'
    AWAITING = 'awaiting', 'Ожидает забора'

    ADOPTED = 'adopted', 'Принят'
    DECLINED = 'declined', 'Отклонен'



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
        default=OrderStatus.IN_PROGRESS
    )
    decline_reason = models.TextField(
        verbose_name='Причина отклонения',
        blank=True,
        null=True,
        default=None
    )
    user = models.ForeignKey(
        verbose_name='Пользователь',
        to='User',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(
        verbose_name='Время создания',
        auto_now_add=True,
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'id: {self.id} user: {self.user.username} status: {self.status} products_count: {self.products.count()}'


class CartProduct(models.Model):
    product = models.ForeignKey(
        verbose_name='Изделие производства',
        to='ProductCompany',
        on_delete=models.CASCADE
    )
    count = models.PositiveIntegerField(
        verbose_name='Количество'
    )

    def to_order_product(self):
        return OrderProduct.objects.create(product=self.product, count=self.count)

    class Meta:
        ordering = ('id',)
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'

    def __str__(self):
        return f'id: {self.id}, product: {self.product.name} count: {self.count}'


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

    def get_cart_product(self, product_id):
        product = ProductCompany.objects.get(id=product_id)
        return self.products.get(product=product)

    class Meta:
        ordering = ('id',)
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        return f'id: {self.id} user: {self.user.username} products_count: {self.products.count()}'


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
        null=True,
        default=None
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
        null=True,
        default=None
    )
    image = models.ImageField(
        verbose_name='Фото',
        upload_to='users/',
        blank=True,
        null=True,
        default=None
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


class NotificationType:
    TYPE_TEXT = 'text'
    TYPE_EVALUATION = 'evaluation'
    TYPE_ORDER = 'order'
    TYPE_DELIVERED = 'delivered'
    TYPE_CAN_COMMENT = 'can_comment'


class Notification(models.Model):
    user = models.ForeignKey(
        verbose_name='Пользователь',
        to='User',
        on_delete=models.CASCADE
    )
    text = models.TextField(
        verbose_name='Текст'
    )
    type = models.CharField(
        verbose_name='Тип уведомления',
        max_length=255
    )
    additional_data = models.JSONField(
        verbose_name='Дополнительные данные',
        blank=True,
        null=True,
        default=None
    )
    is_read = models.BooleanField(
        verbose_name='Прочитано',
        default=False
    )
    created_at = models.DateTimeField(
        verbose_name='Время создания',
        auto_now_add=True
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'

    def __str__(self):
        return f'id: {self.id}, user: {self.user.username}, is_read: {self.is_read}'
