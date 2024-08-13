from .import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('menu_list/', views.MenuList.as_view(), name='menu_list'),
    ]