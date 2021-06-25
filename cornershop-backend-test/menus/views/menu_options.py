from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from menus.models import Option
from menus.serializers import OptionModelSerializer
from utils.permissions import IsManager


class OptionViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):

    """Option view set."""

    permission_classes = (IsAuthenticated, IsManager)
    queryset = Option.objects.all()
    serializer_class = OptionModelSerializer
