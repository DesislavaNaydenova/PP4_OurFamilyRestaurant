from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Menu, OpeningHour
from django.db.models import Case, When, Value, IntegerField


# Create your views here.

# Homepage view
def index(request):
    # Add custom order to the days of the week
    ordering = Case(
        When(day_of_week='Monday', then=Value(1)),
        When(day_of_week='Tuesday', then=Value(2)),
        When(day_of_week='Wednesday', then=Value(3)),
        When(day_of_week='Thursday', then=Value(4)),
        When(day_of_week='Friday', then=Value(5)),
        When(day_of_week='Saturday', then=Value(6)),
        When(day_of_week='Sunday', then=Value(7)),
        output_field=IntegerField(),
    )
    opening_hours = OpeningHour.objects.annotate(day_order=ordering).order_by('day_order')
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

def reservations(request):
    return render(request, 'reservations.html')