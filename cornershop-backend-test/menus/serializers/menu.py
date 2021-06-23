"""Menus serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from menus.models import Menu

# Option serializers
from .menu_options import OptionModelSerializer


class MenuModelSerializer(serializers.ModelSerializer):
    """Menu model serializer."""

    class Meta:
        """Meta class."""
        model = Menu
        fields = (
            'pk',
            'menu_uuid',
            'name',
            'date',
            'reminder',
            'options',
            'available',
            'created',
            'modified',
        )


class ListMenuModelSerializer(serializers.ModelSerializer):
    """List Menu model serializer."""
    options = OptionModelSerializer(required=True, many=True)

    class Meta:
        """Meta class."""
        model = Menu
        fields = (
            'pk',
            'menu_uuid',
            'name',
            'date',
            'reminder',
            'available',
            'options',
            'created',
            'modified',
        )
