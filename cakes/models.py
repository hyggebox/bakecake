from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
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
            MinValueValidator(1),
            MaxValueValidator(3),
        ]
    )
    price = models.DecimalField(
        verbose_name='Стоимость',
        max_digits=15,
        decimal_places=2
    )

    class Meta:
        verbose_name = 'Уровень торта'
        verbose_name_plural = 'Уровни торта'

    def __str__(self):
        return f'{self.level_count}'


class CakeShape(models.Model):
    CAKE_SHAPE = (
        ('round', 'Круг'),
        ('square', 'Квадрат'),
        ('rectangle', 'Прямоугольник'),
    )
    shape = models.CharField(
        max_length=10,
        verbose_name='Форма',
        choices=CAKE_SHAPE,
        default='round'
    )
    price = models.DecimalField(
        verbose_name='Стоимость',
        max_digits=15,
        decimal_places=2
    )

    class Meta:
        verbose_name = 'Форма торта'
        verbose_name_plural = 'Формы торта'

    def __str__(self):
        return self.get_shape_display()


class CakeTopping(models.Model):
    TOPPING = (
        (None, 'Выберите топпинг'),
        ('white', 'Белый соус'),
        ('caramel', 'Карамельный'),
        ('maple', 'Кленовый'),
        ('blueberry', 'Черничный'),
        ('choco', 'Молочный шоколад'),
        ('strawberry', 'Клубничный'),
    )
    cake_topping = models.CharField(
        max_length=15,
        verbose_name='Топпинг',
        choices=TOPPING,
        blank=True
    )
    price = models.DecimalField(
        verbose_name='Стоимость',
        max_digits=15,
        decimal_places=2
    )

    class Meta:
        verbose_name = 'Топпинг'
        verbose_name_plural = 'Топпинги'

    def __str__(self):
        return self.get_cake_topping_display()


class CakeBerry(models.Model):
    BERRIES = (
        (None, 'Выберите ягоды'),
        ('blackberry', 'Ежевика'),
        ('raspberry', 'Малина'),
        ('blueberry', 'Голубика'),
        ('strawberry', 'Клубника'),
    )
    cake_berry = models.CharField(
        max_length=15,
        verbose_name='Ягоды',
        choices=BERRIES,
        blank=True
    )
    price = models.DecimalField(
        verbose_name='Стоимость',
        max_digits=15,
        decimal_places=2
    )

    class Meta:
        verbose_name = 'Ягода'
        verbose_name_plural = 'Ягоды'

    def __str__(self):
        return self.get_cake_berry_display()


class CakeDecor(models.Model):
    DEC0R = (
        (None, 'Выберите декор'),
        ('pistachios', 'Фисташки'),
        ('meringue', 'Безе'),
        ('hazelnuts', 'Фундук'),
        ('pekan', 'Пекан'),
        ('marshmallow', 'Маршмеллоу'),
        ('marzipan', 'Марципан'),
    )
    cake_decor = models.CharField(
        max_length=15,
        verbose_name='Декор',
        choices=DEC0R,
        blank=True
    )
    price = models.DecimalField(
        verbose_name='Стоимость',
        max_digits=15,
        decimal_places=2
    )

    class Meta:
        verbose_name = 'Декор'
        verbose_name_plural = 'Декор'

    def __str__(self):
        return self.get_cake_decor_display()


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
    berry = models.ManyToManyField(
        CakeBerry,
        verbose_name='Ягоды',
        related_name='berries'
    )
    decor = models.ManyToManyField(
        CakeDecor,
        verbose_name='Декор',
        related_name='decors'
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
    price = models.DecimalField(
        verbose_name='Стоимость',
        max_digits=15,
        decimal_places=2
    )

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-registered_at']

    def __str__(self):
        return f'{self.customer}: {self.registered_at}'
