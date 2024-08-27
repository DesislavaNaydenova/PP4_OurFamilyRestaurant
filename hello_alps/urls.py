from .import views
from django.urls import path
from .views import Login, register, user_reservation

urlpatterns = [
    path('', views.index, name='index'),
    path('menu_list', views.MenuList.as_view(), name='menu_list'),
    path('opening_hours', views.OpeningHour, name='opening_hours'),
    path('reservations/', views.reservations, name='reservations'),
    path('login/', Login.as_view(), name='login_url'),
    path('register/' , register, name='signup_url'),
    path('guest_reservation/', views.guest_reservation, name='guest_reservation'),
    path('user_reservation/', views.user_reservation, name='user_reservation'),
    path('about/', views.about_me, name='about'),
    path('contact/', views.contact, name='contact'),
    path('user_reservations/', views.user_reservations, name='user_reservations'),
    path('edit_reservation/<int:reservation_id>/', views.edit_reservation, name='edit_reservation'),
    path('cancel_reservation/<int:reservation_id>/', views.cancel_reservation, name='cancel_reservation'),
]