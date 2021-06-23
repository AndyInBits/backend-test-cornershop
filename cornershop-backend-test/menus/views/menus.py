# Django
from django.shortcuts import get_object_or_404


# Django Rest Framework
from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins, viewsets
from rest_framework.response import Response

# Local models
from menus.models import Menu
from users.models import User

# Serializers class
from menus.serializers import MenuModelSerializer, ListMenuModelSerializer

# Local permissions
from utils.permissions import IsManager


class MenuViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.ListModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):

    """Menu view set."""
    permission_classes = (IsAuthenticated, IsManager)
    queryset = Menu.objects.all()

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update' or self.action == 'partial_update':
            return MenuModelSerializer
        return ListMenuModelSerializer
