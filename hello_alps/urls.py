from .import views
from django.urls import path
from .views import Login

urlpatterns = [
    path('', views.index, name='index'),
    path('menu_list', views.MenuList.as_view(), name='menu_list'),
    path('opening_hours', views.OpeningHour, name='opening_hours'),
    path('reservations/', views.reservations, name='reservations'),
    path('login/', Login.as_view(), name='login_url'),
    path('register/' , register, name='signup_url')
    ]