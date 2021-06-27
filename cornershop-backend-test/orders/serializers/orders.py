"""Orders serializers."""

from django.contrib.auth import authenticate
from rest_framework import serializers

from menus.models import Menu
from menus.serializers import ListMenuModelSerializer
from orders.models import Order
from orders.tasks import confirm_order_email
from users.serializers import UserModelSerializer


class OrderCreateSerializer(serializers.Serializer):
    menu = serializers.IntegerField()
    comment = serializers.CharField(min_length=1, max_length=500)
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, max_length=64)
    option = serializers.CharField(min_length=0, max_length=500)

    def validate(self, data):
        """Check credentials and menu"""

        user = authenticate(username=data["email"], password=data["password"])
        if not user:
            raise serializers.ValidationError("Invalid credentials")

        try:
            menu = Menu.objects.get(id=data["menu"], available=True)
        except Menu.DoesNotExist:
            raise serializers.ValidationError(
                "This menu is no longer available")

        self.context["user"] = user
        self.context["menu"] = menu

        return data

    def create(self, data):
        # """Handle order creation."""
        order = Order.objects.create(
            menu=self.context["menu"],
            user=self.context["user"],
            comment=data["comment"],
            option=data["option"],
        )
        confirm_order_email.delay(order.pk)
        return order


class OrderModelSerializer(serializers.ModelSerializer):
    """Order model serializer."""

    class Meta:
        """Meta class."""

        model = Order
        fields = (
            "pk",
            "comment",
            "menu",
            "option",
            "created",
            "modified",
        )


class OrderDeatilsModelSerializer(serializers.ModelSerializer):
    """Order model serializer."""

    user = UserModelSerializer(required=True)
    menu = ListMenuModelSerializer(required=True)

    class Meta:
        """Meta class."""

        model = Order
        fields = (
            "pk",
            "comment",
            "user",
            "menu",
            "option",
            "created",
            "modified",
        )
