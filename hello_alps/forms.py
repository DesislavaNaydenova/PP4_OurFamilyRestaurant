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
    # date = forms.DateField(widget=forms.DateInput(format='%Y-%m-%d'), input_formats=['%d-%m-%Y'])
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format='%Y-%m-%d'),
        input_formats=['%d.%m.%Y', '%d-%m-%Y', '%Y-%m-%d']  
    )
    time = forms.ChoiceField(
        widget=forms.Select(attrs={'class':'form-control'}),
        choices=[]
    )
    
    class Meta:
        model = UserReservation
        fields = ['date', 'time', 'table', 'comment']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'date' in self.data:
            try:
                selected_date = datetime.strptime(self.data['date'], '%Y-%m-%d').date()
                self.fields['time'].choices = self.get_time_choices(selected_date)
            except (ValueError, TypeError):
                slef.fields['time'].choices = []

    def get_time_choices(selected_date):
                day_of_week = selected_date.strftime('%A')
                opening_hours = OpeningHour.objects.filter(day_of_week=day_of_week)

                time_choices = []
                for hour in opening_hours:
                    start_time = hour.open_time
                    end_time = hour.close_time
                    while start_time < end_time:
                        time_choices.append((start_time, start_time.strftime('%H:%M')))
                        start_time = (datetime.combine(datetime.today(), start_time) + timedelta(minutes=30)).time()

                return time_choices
            