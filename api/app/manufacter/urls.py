from django.urls import path, include


urlpatterns = [
    path('path/', include('api.app.manufacter.path.urls')),
    path('product/', include('api.app.manufacter.product.urls')),
    path('point/', include('api.app.manufacter.point.urls')),
    path('order/', include('api.app.manufacter.order.urls')),
]
