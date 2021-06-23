# Django Rest Framework
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import mixins, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Local models
from menus.models import Menu

# Serializers class
from menus.serializers import MenuModelSerializer, ListMenuModelSerializer

# Local permissions
from utils.permissions import IsManager

# date time lib
from datetime import datetime


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


class GetTodayMenuAPIView(APIView):
    """ Get menu today view """
    permission_classes = (AllowAny,)
    http_method_names = ['get']

    def get(self, request, uuid, format=None):
        try:
            queryset = Menu.objects.get(
                menu_uuid=uuid,
                date=datetime.date(datetime.now()).strftime('%Y-%m-%d'),
                available=True
            )
        except Menu.DoesNotExist:
            return Response({"detail": "Menu not available"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ListMenuModelSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)
