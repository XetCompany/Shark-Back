from django.urls import path, include


urlpatterns = [
    path('products/', include('api.app.customer.products.urls')),
    path('cart/', include('api.app.customer.cart.urls')),
]
