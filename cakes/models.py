from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


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
        return f'{self.level_count} уровень'


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
        return self.shape


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
        return self.cake_topping


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
        return self.cake_berry


class CakeDecor(models.Model):
    DEC0R = (
        (None, 'Выберите декор'),
        ('pistachios', 'Фисташки'),
        ('meringue', 'Безе'),
        ('hazelnuts', 'Фундук'),
        ('pekan', 'Пекан'),
        ('marshmallow', 'Маршмеллоу'),
        ('marshmallow', 'Марципан'),
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
    base_price = models.DecimalField(
        verbose_name='Базовая стоимость',
        max_digits=15,
        decimal_places=2
    )

    class Meta:
        verbose_name = 'Торт'
        verbose_name_plural = 'Торты'

    def __str__(self):
        return f'Торт {self.level_count} уровневый - форма {self.shape}'



