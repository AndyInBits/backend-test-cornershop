# local views
from . import views

# django urls paths
from django.urls import path, include

# Django REST Framework
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'api/v1/menus', views.MenuViewSet, basename='menus')
router.register(r'api/v1/menu/options', views.OptionViewSet,
                basename='menu_options')

urlpatterns = [
    path('', include(router.urls)),
]
