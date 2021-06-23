"""Orders serializers."""

# Django REST Framework
from rest_framework import serializers

# Models Order
from orders.models import Order

# Menu Serializers
from menus.serializers import ListMenuModelSerializer

# User Serializers
from users.serializers import UserModelSerializer


class OrderDetailModelSerializer(serializers.ModelSerializer):
    """Order model serializer."""
    class Meta:
        """Meta class."""
        model = Order
        fields = (
            'pk',
            'comment',
            'user',
            'menu',
            'created',
            'modified',
        )


class OrderModelSerializer(serializers.ModelSerializer):
    """Order model serializer."""

    user = UserModelSerializer(required=True)
    menu = ListMenuModelSerializer(required=True)

    class Meta:
        """Meta class."""
        model = Order
        fields = (
            'pk',
            'comment',
            'user',
            'menu',
            'created',
            'modified',
        )
