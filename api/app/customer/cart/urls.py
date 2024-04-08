from django.urls import path

from . import views

urlpatterns = [
    path('', views.CartView.as_view()),
    path('<int:product_id>/', views.CartProductView.as_view()),
]
