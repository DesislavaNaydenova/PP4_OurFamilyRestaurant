from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Create your models here.


class Menu(models.Model):
    """ Manages the menu items """
    name = models.CharField(max_length=300, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    categories = models.CharField(max_length=50, choices=[
        ('starters', 'Starters'),
        ('maindishes', 'Main dishes'),
        ('pizza', 'Pizza'),
        ('desserts', 'Desserts'),
    ])

    def __str__(self):
        return self.name


class OpeningHour(models.Model):
    """ Manages the opening hours """
    day_of_week = models.CharField( choices=[
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday')
    ])
    open_time = models.TimeField()
    close_time = models.TimeField()

    class Meta:
        ordering = ['day_of_week']
        verbose_name = 'Opening Hour'
        verbose_name_plural = 'Opening Hours'

    def __str__(self):
        return f"{self.day_of_week}: {self.open_time} - {self.close_time}"


class Table(models.Model):
    table_number = models.PositiveIntegerField()
    capacity = models.PositiveIntegerField()
    status = models.CharField(choices= [
        ('available', 'Available'),
        ('reserved', 'Reserved'),
    ], default= 'available')

    class Meta:
        ordering = ['table_number']

    def __str__(self):
        return f"Table: {self.table_number} - Capacity: {self.capacity}"


class UserReservation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    table = models.ForeignKey('Table', on_delete=models.SET_NULL, null=True)
    date = models.DateField(default=timezone.now)
    opening_hour = models.ForeignKey('OpeningHour', on_delete=models.SET_NULL, null=True)
    time =models.TimeField()
    comment = models.TextField(blank=True, max_length=1000)

    class Meta:
        ordering = ['date', 'time']
        verbose_name = 'User Reservation'
        verbose_name_plural = 'User Reservations'

    def __str__(self):
        return f"{self.date} - {self.time} - Table {self.table.table_number} (Capacity {self.table.capacity})"

class About(models.Model):
    title = models.CharField(max_length=200)
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()

    def __str__(self):
        return self.title
