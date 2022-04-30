from django.contrib import admin

from .models import Discounts
from .models import Cake
from .models import Order
from .models import (CakeDecor, CakeBerry, CakeShape, CakeTopping, CakeLevel)
from .models import CustomUser


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'status', 'price', 'cake', 'delivery_date',
                    'deliver_address', 'registered_at', 'delivery_comments',)
    readonly_fields = [
        'registered_at',
    ]
    list_editable = ['status', 'price',]
    raw_id_fields = ['customer', 'cake']


@admin.register(Cake)
class CakeAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'topping', 'berry', 'decor', 'inscription', 'comment')


@admin.register(Discounts)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('discount_name', 'discount_amount')
    list_editable = ['discount_amount']


@admin.register(CakeDecor, CakeBerry, CakeShape, CakeTopping, CakeLevel)
class CakePartsAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'price')
    list_editable = ['price']


class UserInline(admin.TabularInline):
    model = Order
    extra = 0


@admin.register(CustomUser)
class UserAdminConfig(admin.ModelAdmin):
    list_display = ('phonenumber', 'username', 'email', 'is_staff', 'is_admin', 'is_active')
    search_fields = ('phonenumber', 'username', 'email', 'is_active')
    list_filter = ('is_staff', 'is_admin', 'is_active')
    inlines = [UserInline]
