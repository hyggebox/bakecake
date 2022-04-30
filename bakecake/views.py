import string

from django.db import transaction
from django.core.mail import EmailMessage

from django.contrib.auth.decorators import login_required
from django.utils.crypto import get_random_string

from django.shortcuts import render

from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response

from cakes.models import (Cake, CustomUser, Order,
                          CakeLevel, CakeShape, CakeTopping,
                          CakeDecor, CakeBerry)


def generate_password():
    psw_length = 5
    allowed_chars = string.ascii_lowercase + string.digits
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

    return order.id


def render_index_page(request):
    levels_query_set = CakeLevel.objects.values_list('level_count')
    levels_names = [level[0] for level in levels_query_set]

    shapes_query_set = CakeShape.objects.values_list('shape')
    shapes_names = [shape[0] for shape in shapes_query_set]

    toppings_query_set = CakeTopping.objects.values_list('cake_topping')
    toppings_names = [topping[0] for topping in toppings_query_set]

    decors_query_set = CakeDecor.objects.values_list('cake_decor')
    decors_names = [decor[0] for decor in decors_query_set]

    berries_query_set = CakeBerry.objects.values_list('cake_berry')
    berries_names = [berry[0] for berry in berries_query_set]

    context = {
        'levels_names': levels_names,
        'shapes_names': shapes_names,
        'toppings_names': toppings_names,
        'decors_names': decors_names,
        'berries_names': berries_names
    }

    return render(request, 'index.html', context=context)


@login_required(login_url='/auth/login/')
def render_lk_page(request):
    template = 'lk.html'

    return render(request, template)


@transaction.atomic
@api_view(['GET', 'POST', 'PUT'])
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
            order_id = create_order(order_data, customer_id, cake_id)

        return Response(order_id)

    if request.method == 'GET':
      
        levels_query_set = CakeLevel.objects.values_list('level_count', 'price')
        levels_names = [level[0] for level in levels_query_set]
        levels_prices = [level[1] for level in levels_query_set]

        shapes_query_set = CakeShape.objects.values_list('shape', 'price')
        shapes_names = [shape[0] for shape in shapes_query_set]
        shapes_prices = [shape[1] for shape in shapes_query_set]

        toppings_query_set = CakeTopping.objects.values_list('cake_topping', 'price')
        toppings_names = [topping[0] for topping in toppings_query_set]
        toppings_prices = [topping[1] for topping in toppings_query_set]

        decors_query_set = CakeDecor.objects.values_list('cake_decor', 'price')
        decors_names = [decor[0] for decor in decors_query_set]
        decors_prices = [decor[1] for decor in decors_query_set]

        berries_query_set = CakeBerry.objects.values_list('cake_berry', 'price')
        berries_names = [berry[0] for berry in berries_query_set]
        berries_prices = [berry[1] for berry in berries_query_set]

        cake_data = {
            'levels_names': levels_names,
            'levels_prices': levels_prices,

            'shapes_names': shapes_names,
            'shapes_prices': shapes_prices,

            'toppings_names': toppings_names,
            'toppings_prices': toppings_prices,

            'decors_names': decors_names,
            'decors_prices': decors_prices,
            
            'berries_names': berries_names,
            'berries_prices': berries_prices
        }

        return Response(cake_data)

    if request.method == 'PUT':
        order = Order.objects.get(id=request.data['orderId'])
        order.status = 'pay'
        order.save()

        return Response('OK')


def success_page(request):
    return render(request, 'success.html')

