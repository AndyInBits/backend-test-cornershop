# local views
from . import views

# django urls paths
from django.urls import path, include

# Django REST Framework
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'api/v1/orders', views.OrdersViewSet, basename='orders')

urlpatterns = [
    path('', include(router.urls)),
]
