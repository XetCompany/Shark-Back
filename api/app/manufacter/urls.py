from django.urls import path, include


urlpatterns = [
    path('path/', include('api.app.manufacter.path.urls')),
]
