from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Menu


# Create your views here.

# Homepage view
def index(request):
    return render(request, 'hello_alps/index.html')

# Menu List View
class MenuList(generic.ListView):
    queryset = Menu.objects.all()
    template_name = "hello_alps/templates/hello_alps/menu_list.html"