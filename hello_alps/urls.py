from .import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('menu_list', views.MenuList.as_view(), name='menu_list'),
    path('opening_hours', views.OpeningHour, name='opening_hours'),
    path('reservations/', views.reservations, name='reservations'),
    ]