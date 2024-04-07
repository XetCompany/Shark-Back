from django.urls import path, include

from . import views


urlpatterns = [
    path('', views.PathView.as_view()),
    path('<int:path_id>/', views.PathDetailView.as_view()),
]
