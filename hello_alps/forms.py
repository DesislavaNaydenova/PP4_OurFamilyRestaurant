from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import OpeningHour, Table, UserReservation
from datetime import timedelta, datetime


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
    
    class Meta:
        model = UserReservation
        fields = ['date', 'time', 'table', 'comment']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'format': '%Y-%m-%d'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #get the opening hours for the selected day 
        if 'date' in self.data:
            selected_date_str = self.data.get('date')
            try:
                selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()
                day_of_week = selected_date.strftime('%A')
                opening_hours = OpeningHour.objects.filter(day_of_week=day_of_week)

                time_choices = []
                for hour in opening_hours:
                    start_time = hour.open_time
                    end_time = hour.close_time
                    while start_time < end_time:
                        time_choices.append((start_time, start_time.strftime('%H:%M')))
                        start_time = (datetime.combine(datetime.today(), start_time) + timedelta(minutes=30)).time()

                self.fields['time'].choices = time_choices
            except ValueError:
                self.fields['time'].choices =[]
        else:
            self.fields['time'].choices = []
            