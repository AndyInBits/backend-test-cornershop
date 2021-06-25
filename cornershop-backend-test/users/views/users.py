from rest_framework import mixins, viewsets
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from users.models import User
from users.serializers import UserModelSerializer


class GetMeAPIView(RetrieveAPIView):
    """ Get data auth user view """

    permission_classes = (IsAuthenticated,)
    serializer_class = UserModelSerializer

    def get_object(self):
        return self.request.user


class UserViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):

    """User view set."""

    permission_classes = (
        IsAuthenticated,
        IsAdminUser,
    )
    serializer_class = UserModelSerializer
    queryset = User.objects.all()
