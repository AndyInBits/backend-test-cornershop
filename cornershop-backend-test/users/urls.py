# local views
from . import views
# rest framework get token
from rest_framework_simplejwt import views as jwt_views
# django urls paths
from django.urls import path, include

# Django REST Framework
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', views.UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('login', jwt_views.TokenObtainPairView.as_view(), name='users_login'),
    path('token/refresh', jwt_views.TokenRefreshView.as_view(),
         name='users_refresh_token'),
    path('get/me', views.GetMeAPIView.as_view(), name='users_get_me'),

]
