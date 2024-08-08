from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Menu(models.Model):
    """ Manages the menu items """
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    categories = models.CharField(max_length=50, choices=[
        ('starters', 'Starters'),
        ('maindishes', 'Main dishes'),
        ('deserts', 'Deserts'),
    ])

    def __str__(self):
        return self.name