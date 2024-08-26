from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.views import generic
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.db.models import Case, When, Value, IntegerField
from django.urls import reverse_lazy
from .models import Menu, OpeningHour, UserReservation, About
from .forms import FormCreation, UserReservationForm
from datetime import datetime


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
    context_object_name = 'sort_menu_items'
    template_name = 'hello_alps/menu_list.html'

    def get_queryset(self):
        ordered_categories = ['starters', 'maindishes', 'pizza', 'desserts']
        sort_menu_items = {category: Menu.objects.filter(categories=category) for category in ordered_categories}
        return sort_menu_items


# Added to index
# Opening Hours View
#def OpeningHours(request):
#    opening_hours = OpeningHour.objects.all()
#  return render(request, 'hello_alps/index.html', {'opening_hours': opening_hours})
 

# Reservations.html View
def reservations(request):
    return render(request, 'hello_alps/reservations.html')


# guest_reservation.html View
def guest_reservation(request):
    return render(request, 'hello_alps/guest_reservation.html')


# user_reservation.html View
@login_required
def user_reservation(request):
    if request.method == 'POST':
        print(request.POST) # Debugging
        form = UserReservationForm(request.POST)
        if form.is_valid():
            print("Form is valid, processing reservation...") # Debugging
            reservation = form.save(commit= False)
            reservation.user = request.user
            reservation.save()
            print("Reservation saved.") # Debugging
            return render(request, 'hello_alps/user_reservation.html', {
                'form': UserReservationForm(),
                'success': True,
                'reservation_date': reservation.date,
                'reservation_time': reservation.time,
            })
        else:
            print("Form errors:", form.errors) # Debugging
            return render(request, 'hello_alps/user_reservation.html', {'form':form})
            
    form = UserReservationForm()

    if 'date' in request.GET:
        try:
            selected_date = datetime.strptime(request.GET['date'], '%Y-%m-%d').date()
            time_choices = get_time_choices(selected_date)
            form.fields['time'].choices = time_choices
        except ValueError:
            messages.error(request, "Invalida date format.")

    return render(request, 'hello_alps/user_reservation.html', {'form': form})
    

# Login View
class Login(LoginView):
    template_name = 'hello_alps/login.html'
    success_url = reverse_lazy('home')


# Register View
def register(request):
    if request.method == 'POST':
        form = FormCreation(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('user_reservation')
    else:
        form = FormCreation()
    return render(request, 'hello_alps/register.html', {'form': form})

# About View
def about_me(request):
    about = About.objects.all().order_by('-updated_on').first()

    return render(
        request, "hello_alps/about.html", {"about": about},
    )
