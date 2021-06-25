"""Options serializers."""

from rest_framework import serializers

from menus.models import Option


class OptionModelSerializer(serializers.ModelSerializer):
    """Options model serializer."""

    class Meta:
        """Meta class."""

        model = Option
        fields = (
            "pk",
            "option",
            "created",
            "modified",
        )
