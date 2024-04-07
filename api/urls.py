from django.urls import path, include

urlpatterns = [
    path('auth/', include('api.auth.urls')),
    path('app/', include('api.app.urls')),
]
