from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy
from phonenumber_field.modelfields import PhoneNumberField


class Discounts(models.Model):
    discount_name = models.CharField(
        max_length=10,
        verbose_name='Купон'
    )
    discount_amount = models.DecimalField(
        verbose_name='Размер скидки',
        max_digits=3,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(1)]
    )

    class Meta:
        verbose_name = 'Купон'
        verbose_name_plural = 'Купоны'

    def __str__(self):
        return f'Купон {self.discount_name} = {self.discount_amount * 100}%'


class CakeLevel(models.Model):
    level_count = models.IntegerField(
        verbose_name='Количество уровней',
        validators=[
            MinValueValidator(1)
        ]
    )
    price = models.IntegerField(
        verbose_name='Стоимость',
    )

    class Meta:
        verbose_name = 'Уровень торта'
        verbose_name_plural = 'Уровни торта'

    def __str__(self):
        return f'{self.level_count}'


class CakeShape(models.Model):
    shape = models.CharField(
        max_length=50,
        verbose_name='Форма',
    )
    price = models.IntegerField(
        verbose_name='Стоимость',
    )

    class Meta:
        verbose_name = 'Форма торта'
        verbose_name_plural = 'Формы торта'

    def __str__(self):
        return self.shape


class CakeTopping(models.Model):
    cake_topping = models.CharField(
        max_length=50,
        verbose_name='Топпинг',
    )
    price = models.IntegerField(
        verbose_name='Стоимость',
    )

    class Meta:
        verbose_name = 'Топпинг'
        verbose_name_plural = 'Топпинги'

    def __str__(self):
        return self.cake_topping


class CakeBerry(models.Model):
    cake_berry = models.CharField(
        max_length=15,
        verbose_name='Ягоды',
    )
    price = models.IntegerField(
        verbose_name='Стоимость',
    )

    class Meta:
        verbose_name = 'Ягода'
        verbose_name_plural = 'Ягоды'

    def __str__(self):
        return self.cake_berry


class CakeDecor(models.Model):
    cake_decor = models.CharField(
        max_length=15,
        verbose_name='Декор'
    )
    price = models.IntegerField(
        verbose_name='Стоимость',
    )

    class Meta:
        verbose_name = 'Декор'
        verbose_name_plural = 'Декор'

    def __str__(self):
        return self.cake_decor


class Cake(models.Model):
    level_count = models.ForeignKey(
        CakeLevel,
        verbose_name='Количество уровней торта',
        related_name='levels',
        on_delete=models.CASCADE
    )
    shape = models.ForeignKey(
        CakeShape,
        verbose_name='Форма торта',
        related_name='shapes',
        on_delete=models.CASCADE
    )
    topping = models.ForeignKey(
        CakeTopping,
        verbose_name='Топпинг',
        related_name='toppings',
        on_delete=models.CASCADE
    )
    berry = models.ForeignKey(
        CakeBerry,
        verbose_name='Ягоды',
        related_name='berries',
        on_delete=models.CASCADE
    )
    decor = models.ForeignKey(
        CakeDecor,
        verbose_name='Декор',
        related_name='decors',
        on_delete=models.CASCADE
    )
    inscription = models.CharField(
        max_length=200,
        verbose_name='Надпись на торте',
        blank=True
    )
    comment = models.TextField(
        verbose_name='Комментарий',
        blank=True
    )

    class Meta:
        verbose_name = 'Торт'
        verbose_name_plural = 'Торты'

    def __str__(self):
        return f'Торт {self.level_count} уровневый - форма {self.shape}'


class Customer(models.Model):
    firstname = models.CharField(
        'Имя',
        max_length=50,
        null=False
    )
    lastname = models.CharField(
        'Фамилия',
        max_length=50,
        null=False
    )
    phonenumber = PhoneNumberField(
        verbose_name='Телефонный номер'
    )
    email = models.EmailField(
        verbose_name='Email заказчика'
    )
    address = models.CharField(
        max_length=150,
        verbose_name='Адрес заказчика'
    )

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return f'{self.firstname} {self.lastname}'


class Order(models.Model):
    STATUS = (
        ('n', 'Новый'),
        ('a', 'Принят'),
        ('p', 'Готовится'),
        ('d', 'Передан в доставку'),
        ('c', 'Выполнен'),
    )

    customer = models.ForeignKey(
        Customer,
        verbose_name='Заказчик',
        related_name='customers',
        on_delete=models.CASCADE
    )
    cake = models.ForeignKey(
        Cake,
        verbose_name='Заказанный торт',
        related_name='cakes',
        on_delete=models.PROTECT,
    )
    status = models.CharField(
        max_length=20,
        verbose_name='Статус заказа',
        choices=STATUS,
        default='s'
    )
    registered_at = models.DateTimeField(
        'Время регистрации заказа',
        auto_now_add=True,
        db_index=True
    )
    called_at = models.DateTimeField(
        'Время звонка клиенту',
        blank=True,
        null=True,
        db_index=True
    )
    delivered_at = models.DateTimeField(
        'Время доставки заказа',
        blank=True,
        null=True,
        db_index=True
    )
    price = models.IntegerField(
        verbose_name='Стоимость',
    )

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-registered_at']

    def __str__(self):
        return f'{self.customer}: {self.registered_at}'



class CustomUserManager(BaseUserManager):

    def create_user(self, phonenumber, email, username, password,
                    **other_fields):

        email = self.normalize_email(email)

        user = self.model(phonenumber=phonenumber,
                          email=email,
                          username=username,
                          **other_fields)
        user.set_password(password)
        user.save()
        return user


    def create_superuser(self, phonenumber, email, username, password,
                         **other_fields):

        other_fields.setdefault('is_admin', True)
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_superuser', True)

        return self.create_user(phonenumber, email, username, password, **other_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    phonenumber = PhoneNumberField(gettext_lazy('номер телефона'), unique=True)
    email = models.EmailField(
                        verbose_name='email',
                        max_length=255,
                        unique=True,
                    )
    username = models.CharField(
        verbose_name='имя',
        max_length=150
    )

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phonenumber'
    REQUIRED_FIELDS = ['email', 'username']

    def __str__(self):
         return self.username

    class Meta:
        verbose_name = 'Пользователя'
        verbose_name_plural = '_ПОЛЬЗОВАТЕЛИ'
