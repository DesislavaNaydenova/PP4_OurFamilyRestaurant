from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Menu


# Create your views here.

class MenuList(generic.ListView):
    queryset = Menu.objects.all()
    template_name = "index.html"