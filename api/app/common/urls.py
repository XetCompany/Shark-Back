from django.urls import path, include

from . import views


urlpatterns = [
    path('account/', views.account_view),
    path('cities/', views.cities_view),
    path('categories/', views.categories_view),
]
