from django.urls import path

from . import views


urlpatterns = [
    path('', views.OrderView.as_view()),

    path('make/<int:search_info_id>/', views.OrderSearchInfoView.as_view()),
]
