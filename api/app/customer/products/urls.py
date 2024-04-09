from django.urls import path

from . import views

urlpatterns = [
    path('', views.ProductsView.as_view()),
    path('<int:product_id>/', views.ProductInfoView.as_view()),

    path('<int:product_id>/evaluate/', views.ProductEvaluateView.as_view()),
]
