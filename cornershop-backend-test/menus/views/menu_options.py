# Django Rest Framework
from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins, viewsets

# Local models
from menus.models import Option

# Serializers class
from menus.serializers import OptionModelSerializer

# Local permissions
from utils.permissions import IsManager


class OptionViewSet(mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.ListModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):

    """Option view set."""
    permission_classes = (IsAuthenticated, IsManager)
    queryset = Option.objects.all()
    serializer_class = OptionModelSerializer
