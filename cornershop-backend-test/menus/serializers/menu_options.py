"""Options serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from menus.models import Menu, Option


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
