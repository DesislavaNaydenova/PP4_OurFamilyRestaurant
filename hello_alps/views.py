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
    context_object_name = "sort_menu_items"
    template_name = "hello_alps/menu_list.html"

    def get_queryset(self):
        ordered_categories = ["starters", "maindishes", "pizza", "desserts"]
        sort_menu_items = {category: Menu.objects.filter(categories=category) for category in ordered_categories}
        return sort_menu_items


# Added to index
# Opening Hours View
#def OpeningHours(request):
#    opening_hours = OpeningHour.objects.all()
#  return render(request, 'hello_alps/index.html', {'opening_hours': opening_hours})