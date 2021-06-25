from django.urls import include, path
from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt import views as jwt_views

from . import views

router = DefaultRouter()
router.register(r"api/v1/users", views.UserViewSet, basename="users")

urlpatterns = [
    path("", include(router.urls)),
    path("api/v1/login", jwt_views.TokenObtainPairView.as_view(), name="users_login"),
    path(
        "api/v1/token/refresh",
        jwt_views.TokenRefreshView.as_view(),
        name="users_refresh_token",
    ),
    path("api/v1/get/me", views.GetMeAPIView.as_view(), name="users_get_me"),
]
