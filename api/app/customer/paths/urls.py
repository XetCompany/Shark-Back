from django.urls import path

from . import views

urlpatterns = [
    path('<int:pickup_point_id>/', views.PickupPointPathsView.as_view()),
]
