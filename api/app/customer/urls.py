from django.urls import path, include


urlpatterns = [
    path('products/', include('api.app.customer.products.urls')),
    path('cart/', include('api.app.customer.cart.urls')),
    path('pickup_points/', include('api.app.customer.pickup_points.urls')),
    path('paths/', include('api.app.customer.paths.urls')),
    path('orders/', include('api.app.customer.orders.urls')),
]
