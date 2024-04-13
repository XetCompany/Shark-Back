from django.urls import path, include

from . import views


notifications_urlpatterns = [
    path('', views.NotificationsView.as_view()),
    path('read/', views.ReadNotificationView.as_view()),
]


urlpatterns = [
    path('account/', views.AccountView.as_view()),
    path('cities/', views.cities_view),
    path('categories/', views.categories_view),

    path('notifications/', include(notifications_urlpatterns)),
]
