# Django Rest Framework
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import mixins, viewsets

# Local permissions
from utils.permissions import IsManager

# Local models
from orders.models import Order

# Serializers class
from orders.serializers import OrderDetailModelSerializer, OrderModelSerializer


class OrdersViewSet(mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.ListModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):

    """Menu view set."""

    def get_serializer_class(self):
        """Assign serializers class based on action."""
        if self.action == 'create' or self.action == 'update' or self.action == 'partial_update':
            return OrderDetailModelSerializer
        return OrderModelSerializer

    def get_queryset(self):
        """queryset based in rol user"""
        if self.request.user.is_manager:
            queryset = Order.objects.all()
        else:
            queryset = Order.objects.filter(user=self.request.user)

        return queryset

    def get_permissions(self):
        """Assign permission based on action."""
        permissions = [IsAuthenticated, ]
        if self.action in ['update', 'partial_update', 'destroy']:
            permissions.append(IsManager)
        return [p() for p in permissions]