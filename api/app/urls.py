from django.urls import path, include


urlpatterns = [
    path('manufacter/', include('api.app.manufacter.urls')),
    path('customer/', include('api.app.customer.urls')),
    path('common/', include('api.app.common.urls')),
]
