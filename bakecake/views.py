import string

from django.db import transaction
from django.core.mail import EmailMessage
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from django.contrib.auth.decorators import login_required
from django.utils.crypto import get_random_string

from cakes.models import (Cake, CustomUser, Order,
                          CakeLevel, CakeShape, CakeTopping,
                          CakeDecor, CakeBerry)


def generate_password():
    psw_length = 8
    allowed_chars = string.ascii_lowercase+string.ascii_uppercase + string.digits
    password = get_random_string(psw_length, allowed_chars=allowed_chars)
    return password


def create_cake(order_data):
    cake = Cake.objects.create(
        level_count=CakeLevel.objects.get(level_count=order_data['Levels']),
        shape=CakeShape.objects.get(shape=order_data['Form']),
        topping=CakeTopping.objects.get(cake_topping=order_data['Topping']),
        berry=CakeBerry.objects.get(cake_berry=order_data['Berries']),
        decor=CakeDecor.objects.get(cake_decor=order_data['Decor']),
        inscription=order_data['Words'],
        comment=order_data['Comments']
    )

    return cake


def create_order(order_data, customer_id, cake_id):
    order = Order.objects.create(
        customer=CustomUser.objects.get(pk=customer_id),
        cake=Cake.objects.get(pk=cake_id),
        status='n',
        delivery_date=f'{order_data["Dates"]} {order_data["Time"]}',
        price=order_data['Cost'],
        deliver_address=order_data['Address'],
        delivery_comments=order_data['DelivComments']
    )


def render_index_page(request):
    levels_query_set = CakeLevel.objects.values_list('level_count')
    levels = [level[0] for level in levels_query_set]

    return render(request, 'index.html')


@login_required(login_url='/auth/login/')
def render_lk_page(request):
    template = 'lk.html'

    return render(request, template)


class CakeLevelSerializer(ModelSerializer):
    class Meta:
        model = CakeLevel
        fields = ('id', 'level_count', 'price')


class CakeShapeSerializer(ModelSerializer):
    class Meta:
        model = CakeShape
        fields = ('id', 'shape', 'price')


class CakeToppingSerializer(ModelSerializer):
    class Meta:
        model = CakeTopping
        fields = ('id', 'cake_topping', 'price')


class CakeDecorSerializer(ModelSerializer):
    class Meta:
        model = CakeDecor
        fields = ('id', 'cake_decor', 'price')


class CakeBerrySerializer(ModelSerializer):
    class Meta:
        model = CakeBerry
        fields = ('id', 'cake_berry', 'price')


@transaction.atomic
@api_view(['GET', 'POST'])
def cake_api(request):

    if request.method == 'POST':

        order_data = request.data

        phone = order_data['Phone']
        password = generate_password()

        try:
            customer = CustomUser.objects.get(phonenumber=phone)

        except CustomUser.DoesNotExist:
            customer = CustomUser.objects.create_user(
                password=password,
                phonenumber=phone,
                email=order_data['Email'],
                username=order_data['Name'],
            )

            message = f'Ваш пароль: {password}'
            EmailMessage(
                subject=message,
                body=message,
                to=[order_data['Email']],
            ).send()

        finally:
            print('create cake')
            cake = create_cake(order_data)
            customer_id = customer.pk
            cake_id = cake.pk
            create_order(order_data, customer_id, cake_id)

        return Response(23)

    if request.method == 'GET':
        levels = CakeLevel.objects.all()
        shapes = CakeShape.objects.all()
        toppings = CakeTopping.objects.all()
        decors = CakeDecor.objects.all()
        berries = CakeBerry.objects.all()

        level_prices = [
            level['price'] for level in CakeLevelSerializer(levels, many=True).data
        ]
        shape_prices = [
            shape['price'] for shape in CakeShapeSerializer(shapes, many=True).data
        ]
        topping_prices = [
            topping['price'] for topping in CakeToppingSerializer(toppings, many=True).data
        ]
        decor_prices = [
            decor['price'] for decor in CakeDecorSerializer(decors, many=True).data
        ]
        berry_prices = [
            berry['price'] for berry in CakeBerrySerializer(berries, many=True).data
        ]

        components = {
            'levels': level_prices,
            'shapes': shape_prices,
            'toppings': topping_prices,
            'decors': decor_prices,
            'berries': berry_prices,
        }

        return Response(components)
