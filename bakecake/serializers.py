from rest_framework.serializers import ModelSerializer

from cakes.models import (CakeLevel, CakeShape, CakeTopping, CakeDecor,
                                                             CakeBerry)


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