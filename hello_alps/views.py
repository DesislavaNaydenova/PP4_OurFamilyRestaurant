from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.views import generic
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.db.models import Case, When, Value, IntegerField
from django.urls import reverse_lazy
from .models import Menu, OpeningHour, UserReservation, About
from .forms import FormCreation, UserReservationForm, GuestReservationForm
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
    return render(request,
                  'hello_alps/index.html', {'opening_hours': opening_hours})


# Menu List View
class MenuList(generic.ListView):
    context_object_name = 'sort_menu_items'
    template_name = 'hello_alps/menu_list.html'

    def get_queryset(self):
        ordered_categories = ['starters', 'maindishes', 'pizza', 'desserts']
        sort_menu_items = {category: Menu.objects.filter(categories=category)
                           for category in ordered_categories}
        return sort_menu_items


# Reservations.html View
def reservations(request):
    return render(request, 'hello_alps/reservations.html')


# guest_reservation.html View
def guest_reservation(request):
    if request.method == 'POST':
        form = GuestReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save()

            request.session['reservation_success'] = True
            request.session['reservation_date'] = reservation.date.strftime('%Y.%m.%d')
            request.session['reservation_time'] = reservation.time.strftime('%H:%M')

            return redirect('guest_reservation')
        else:
            return render(request,
                          'hello_alps/guest_reservation.html', {'form': form})

    else:
        form = GuestReservationForm()

    reservation_success = request.session.pop('reservation_success', False)
    reservation_date = request.session.pop('reservation_date', '')
    reservation_time = request.session.pop('reservation_time', '')

    return render(request, 'hello_alps/guest_reservation.html', {
        'form': form,
        'reservation_success': reservation_success,
        'reservation_date': reservation_date,
        'reservation_time': reservation_time,
        })


# user_reservation.html View
@login_required
def user_reservation(request):
    if request.method == 'POST':
        post_data = request.POST.copy()
        date_str = post_data.get('date')

        if date_str:
            formatted_date = datetime.strptime(date_str, '%Y-%m-%d').strftime('%Y-%m-%d')
            post_data['date'] = formatted_date

        if 'reservation_id' in request.POST:
            reservation = UserReservation.objects.get(pk=request.POST['reservation_id'])
            form = UserReservationForm(post_data, isinstance=reservation)

        form = UserReservationForm(post_data)

        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.save()

            request.session['reservation_success'] = True
            request.session['reservation_date'] = reservation.date.strftime('%Y.%m.%d')
            request.session['reservation_time'] = reservation.time.strftime('%H:%M')

            return redirect('user_reservations')
        else:
            return render(request,
                          'hello_alps/user_reservation.html', {'form': form})

    else:
        form = UserReservationForm()

        if 'date' in request.GET:
            try:
                selected_date = datetime.strptime(request.GET['date'], '%Y-%m-%d').date()
                form.fields['time'].choices = form.get_time_choices(selected_date)
            except ValueError:
                messages.error(request, "Invalida date format.")

    return render(request, 'hello_alps/user_reservation.html', {'form': form})


# Reservation management
@login_required
def user_reservations(request):
    reservations = UserReservation.objects.filter(user=request.user,
                                                  date__gte=datetime.today()).order_by('date')

    # Retrieve session flags
    reservation_success = request.session.pop('reservation_success', False)
    edit_success = request.session.pop('edit_success', False)
    reservation_date = request.session.pop('reservation_date', None)
    reservation_time = request.session.pop('reservation_time', None)
    cancel_warning = request.session.pop('cancel_warning', False)

    return render(request, 'hello_alps/user_reservations.html', {
        'reservations': reservations,
        'reservation_success': reservation_success,
        'reservation_date': reservation_date,
        'reservation_time': reservation_time,
        'edit_success': edit_success,
        'cancel_warning': cancel_warning,
        })


# Edit reservation View
@login_required
def edit_reservation(request, reservation_id):
    reservation = get_object_or_404(UserReservation, id=reservation_id, user=request.user)

    if request.method == 'POST':
        form = UserReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            updated_reservation = form.save()
            request.session['edit_success'] = True
            request.session['reservation_date'] = updated_reservation.date.strftime('%Y.%m.%d')
            request.session['reservation_time'] = updated_reservation.time.strftime('%H:%M')
            return redirect('user_reservations')
    else:
        form = UserReservationForm(instance=reservation)

    return render(request, 'hello_alps/edit_reservation.html', {
        'form': form,
        'reservation': reservation
        })


# Cancel reservation View
@login_required
def cancel_reservation(request, reservation_id):
    reservation = get_object_or_404(UserReservation,
                                    id=reservation_id, user=request.user)
    reservation.delete()
    request.session['cancel_warning'] = True
    return redirect('user_reservations')


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


# contact.html View
def contact(request):
    return render(request, 'hello_alps/contact.html')
