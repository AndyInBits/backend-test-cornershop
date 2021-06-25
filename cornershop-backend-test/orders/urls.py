from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r"api/v1/orders", views.OrdersViewSet, basename="orders")

urlpatterns = [
    path("", include(router.urls)),
]
