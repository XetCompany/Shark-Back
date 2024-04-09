from django.urls import path

from . import views

urlpatterns = [
    path('', views.PickupPointsView.as_view()),
]
