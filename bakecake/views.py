import string

from django.contrib.auth.decorators import login_required
from django.utils.crypto import get_random_string
from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response

from cakes.models import (CakeLevel, CakeShape, CakeTopping, CakeDecor,
                                                             CakeBerry)


def generate_password():
    psw_length = 8
    allowed_chars = string.ascii_lowercase+string.ascii_uppercase + string.digits
    password = get_random_string(psw_length, allowed_chars=allowed_chars)
    return password


def render_index_page(request):
    levels_query_set = CakeLevel.objects.values_list('level_count')
    levels_names = [level[0] for level in levels_query_set]

    context = {
        'levels_names': levels_names
    }

    return render(request, 'index.html', context=context)


@login_required(login_url='/auth/login/')
def render_lk_page(request):
    template = 'lk.html'
    # template = 'lk-order.html'
    return render(request, template)


@api_view(['GET', 'POST'])
def cake_api(request):
    if request.method == 'POST':
        return Response(23)

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
