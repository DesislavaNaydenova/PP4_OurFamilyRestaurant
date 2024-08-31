from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import OpeningHour, Table, UserReservation
from datetime import timedelta, datetime
from django.core.exceptions import ValidationError


class FormCreation(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.help_text = None
            field.widget.attrs.update({'class': 'form-control'})


class UserReservationForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format='%Y-%m-%d'),
        input_formats=['%d.%m.%Y', '%d-%m-%Y', '%Y-%m-%d']  
    )
    
    class Meta:
        model = UserReservation
        fields = ['date', 'time', 'table', 'comment']
        widgets = {
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # If date is provided, populate time choices based on opening hours
        if 'selected_date' in self.data:
            selected_date = self.data.get('selected_date')
            self.fields['time'].choices = self.get_time_choices(selected_date)

    def get_time_choices(self, selected_date):
        # Get day of week for selected date
        day_of_week = selected_date.strftime('%A')
        # Retrive opening hours for given day
        opening_hours = OpeningHour.objects.filter(day_of_week=day_of_week)
        # If no opening hours are available for the selected day, return an empty list
        if not opening_hours.exists():
            return []

        # Generate time slots within opening
        time_choices = []
        for hour in opening_hours:
            start_time = hour.open_time
            end_time = hour.close_time
            while start_time < end_time:
                # Check if table is availablefor the entire day
                if not UserReservation.objects.filter(date=selected_date, table=self.cleaned_data.get('table')).exists():
                    time_choices.append((start_time.strftime('%H:%M'), start_time.strftime('%H:%M')))
                start_time = (datetime.combine(datetime.today(), start_time) + timedelta(minutes=30)).time()

        return time_choices

    def clean_date(self):
        date = self.cleaned_data['date']
        day_of_week = date.strftime('%A')
        opening_hours = OpeningHour.objects.filter(day_of_week=day_of_week)
        
        if not opening_hours.exists():
            raise ValidationError(f'Our restaurant is closed on {day_of_week}s.')

        return date

    def clean_table(self):
        table = self.cleaned_data.get('table')
        date = self.cleaned_data.get('date')

        if date and table:
            reservattion_id = self.instance.pk

            conflicting_reservations = UserReservation.objects.filter(
                date=date, table=table
                ).exclude(pk=reservattion_id)
            if conflicting_reservations.exists():
                raise ValidationError(f'Table {table.table_number} is already reserved on {date}. Please, choose another table!')

        return table


class GuestReservationForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'id': 'date'}, format='%Y-%m-%d'),
        input_formats=['%Y-%m-%d']  #'%d.%m.%Y', '%d-%m-%Y',
    )
    first_name = forms.CharField(max_length=25, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'given-name'}))
    last_name = forms.CharField(max_length=25, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'family-name'}))
    phone_number = forms.CharField(max_length=15, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'tel'}))

    class Meta:
        model = UserReservation
        fields = ['first_name', 'last_name', 'phone_number', 'date', 'time', 'table']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'id': 'date'}, format='%Y-%m-%d'),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control', 'autocomplete': 'off', 'id': 'time'}),
            'table': forms.Select(attrs={'class': 'form-control', 'autocomplete': 'off'}),
        }
            
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # If date is provided, populate time choices based on opening hours
        if 'selected_date' in self.data:
            selected_date = self.data.get('selected_date')
            self.fields['time'].choices = self.get_time_choices(selected_date)

    def get_time_choices(self, selected_date):
        # Get day of week for selected date
        day_of_week = selected_date.strftime('%A')
        # Retrive opening hours for given day
        opening_hours = OpeningHour.objects.filter(day_of_week=day_of_week)
        # If no opening hours are available for the selected day, return an empty list
        if not opening_hours.exists():
            return []

        # Generate time slots within opening
        time_choices = []
        for hour in opening_hours:
            start_time = hour.open_time
            end_time = hour.close_time
            while start_time < end_time:
                # Check if table is availablefor the entire day
                if not UserReservation.objects.filter(date=selected_date, table=self.cleaned_data.get('table')).exists():
                    time_choices.append((start_time.strftime('%H:%M'), start_time.strftime('%H:%M')))
                start_time = (datetime.combine(datetime.today(), start_time) + timedelta(minutes=30)).time()

        return time_choices

    def clean_table(self):
        # Same logic as in UserReservationForm but without conflict with the user's own reservations.
        table = self.cleaned_data.get('table')
        date = self.cleaned_data.get('date')
        time = self.cleaned_data.get('time')

        if date and time:
            conflicting_reservations = UserReservation.objects.filter(
                date=date, time=time, table=table
                )
            if conflicting_reservations.exists():
                raise ValidationError(f'Table {table.table_number} is already reserved at {time} on {date}. Please, choose another table!')

        return table