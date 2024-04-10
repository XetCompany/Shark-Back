from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include


urlpatterns = [
    path('manufacter/', include('api.app.manufacter.urls')),
    path('customer/', include('api.app.customer.urls')),
    path('common/', include('api.app.common.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
