from django.db import models
from django.contrib.auth.models import User

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