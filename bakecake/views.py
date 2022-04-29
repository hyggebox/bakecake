import string

from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from django.contrib.auth.decorators import login_required
from django.utils.crypto import get_random_string

from cakes.models import (CakeLevel, CakeShape, CakeTopping,
                          CakeDecor, CakeBerry)


def generate_password():
    psw_length = 8
    allowed_chars = string.ascii_lowercase+string.ascii_uppercase + string.digits
    password = get_random_string(psw_length, allowed_chars=allowed_chars)
    return password


def render_index_page(request):
    levels_query_set = CakeLevel.objects.values_list('level_count')
    levels = [level[0] for level in levels_query_set]

    return render(request, 'index.html')


@login_required(login_url='/auth/login/')
def render_lk_page(request):
    template = 'lk.html'
    # template = 'lk-order.html'
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


@api_view(['GET', 'POST'])
def cake_api(request):
    if request.method == 'POST':
        print('WAS POST!!!!')
        return Response(23)
    if request.method == 'GET':
        print('WAS GET')
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
