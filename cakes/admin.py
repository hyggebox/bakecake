from django.contrib import admin

from .models import Discounts
from .models import Cake
from .models import Customer
from .models import Order
from .models import (CakeDecor, CakeBerry, CakeShape, CakeTopping, CakeLevel)
from .models import CustomUser


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    readonly_fields = [
        'registered_at',
    ]


@admin.register(Cake)
class CakeAdmin(admin.ModelAdmin):
    pass

@admin.register(Discounts)
class DiscountAdmin(admin.ModelAdmin):
    pass


@admin.register(CakeDecor, CakeBerry, CakeShape, CakeTopping, CakeLevel)
class CakePartsAdmin(admin.ModelAdmin):
    pass


@admin.register(CustomUser)
class UserAdminConfig(admin.ModelAdmin):
    list_display = ('phonenumber', 'username', 'email', 'is_staff', 'is_admin', 'is_active')
    search_fields = ('phonenumber', 'username', 'email', 'is_active')
    list_filter = ('is_staff', 'is_admin', 'is_active')