from django.urls import path, include

from . import views


urlpatterns = [
    path('', views.PointView.as_view()),
    path('<int:product_id>/', views.PointDetailView.as_view()),
]
