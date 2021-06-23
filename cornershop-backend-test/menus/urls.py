# local views
from . import views

# django urls paths
from django.urls import path, include

# Django REST Framework
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', views.MenuViewSet, basename='menus')

urlpatterns = [
    path('/', include(router.urls)),

]
