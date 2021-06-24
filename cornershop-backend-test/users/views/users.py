# Django Rest Framework
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from rest_framework import mixins, viewsets

# Local models
from users.models import User

# Serializers class
from users.serializers import UserModelSerializer


class GetMeAPIView(RetrieveAPIView):
    """ Get data auth user view """
    permission_classes = (IsAuthenticated,)
    serializer_class = UserModelSerializer

    def get_object(self):
        return self.request.user


class UserViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.ListModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):

    """User view set."""
    # permission_classes = (IsAuthenticated, IsAdminUser,)
    serializer_class = UserModelSerializer
    queryset = User.objects.all()
