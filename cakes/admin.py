from django.contrib import admin

from .models import Discounts
from .models import Cake
from .models import (CakeDecor, CakeBerry, CakeShape, CakeTopping, CakeLevel)


@admin.register(Cake)
class CakeAdmin(admin.ModelAdmin):
    pass

@admin.register(Discounts)
class DiscountAdmin(admin.ModelAdmin):
    pass


@admin.register(CakeDecor, CakeBerry, CakeShape, CakeTopping, CakeLevel)
class CakePartsAdmin(admin.ModelAdmin):
    pass