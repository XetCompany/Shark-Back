from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .register import views

login_urlpatterns = [
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns = [
    path('login/', include(login_urlpatterns)),
    path('signup', views.register_handler),
    path('reset_password/', include('api.auth.reset_password.urls')),
]
