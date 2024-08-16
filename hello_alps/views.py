from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Menu, OpeningHour


# Create your views here.

# Homepage view
def index(request):
    opening_hours = OpeningHour.objects.all()
    return render(request, 'hello_alps/index.html', {'opening_hours': opening_hours})

# Menu List View
class MenuList(generic.ListView):
    queryset = Menu.objects.all()
    template_name = "hello_alps/menu_list.html"

# Added to index
# Opening Hours View
#def OpeningHours(request):
#    opening_hours = OpeningHour.objects.all()
#  return render(request, 'hello_alps/index.html', {'opening_hours': opening_hours})