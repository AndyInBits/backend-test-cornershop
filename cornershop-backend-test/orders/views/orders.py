from rest_framework import mixins, status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from orders.models import Order
from orders.serializers import (
    OrderCreateSerializer,
    OrderDeatilsModelSerializer,
    OrderModelSerializer,
)


class OrdersViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):

    """Menu view set."""

    def get_serializer_class(self):
        """Assign serializers class based on action."""
        if self.action == "update" or self.action == "partial_update":
            return OrderModelSerializer
        return OrderDeatilsModelSerializer

    def get_queryset(self):
        """queryset based in rol user"""
        if self.request.user.is_manager:
            queryset = Order.objects.all()
        else:
            queryset = Order.objects.filter(user=self.request.user)

        return queryset

    def get_permissions(self):
        """Assign permission based on action."""
        permissions = []
        if self.action in ["create"]:
            permissions.append(AllowAny)
        if self.action in ["update", "partial_update", "destroy"]:
            permissions.append(IsAuthenticated)
        return [p() for p in permissions]

    def create(self, request):
        """ create order """
        serializer = OrderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Order created"}, status=status.HTTP_201_CREATED)
