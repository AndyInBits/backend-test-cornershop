from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register(r"api/v1/menus", views.MenuViewSet, basename="menus")
router.register(r"api/v1/menu/options", views.OptionViewSet, basename="menu_options")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "api/v1/today/menu/<str:uuid>",
        views.GetTodayMenuAPIView.as_view(),
        name="get_today_menu",
    ),
]
