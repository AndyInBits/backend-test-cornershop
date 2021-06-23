"""Menus serializers."""

# Django REST Framework
from rest_framework import serializers
from rest_framework.response import Response

# Django
from django.shortcuts import get_object_or_404

# Models
from menus.models import Menu, Option


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
            'created',
            'modified',
        )


class OptionModelSerializer(serializers.ModelSerializer):
    """Options model serializer."""
    class Meta:
        """Meta class."""
        model = Option
        fields = (
            'pk',
            'option',
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
            'options',
            'created',
            'modified',
        )
