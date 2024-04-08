from django.urls import path, include

from . import views


urlpatterns = [
    path('', views.PointView.as_view()),
    path('<int:point_id>/', views.PointDetailView.as_view()),

    path('<int:point_id>/products/', views.PointProductView.as_view()),
    path('<int:point_id>/products/<int:product_id>/', views.PointProductDetailView.as_view()),
]
