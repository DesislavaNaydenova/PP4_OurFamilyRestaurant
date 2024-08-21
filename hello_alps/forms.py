from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import OpeningHour, Table, UserReservation
from datetime import timedelta


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
    capacity = forms.ChoiceField(choices=[(4, '4'), (6, '6'), (8, '8')], label='Select table capacity')

    class Meta:
        model = UserReservation
        fields = ['date', 'time', 'table', 'capacity', 'comment']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #table choices based on capacity
        if 'capacity' in self.data:
            try:
                selected_capacity = int(self.data.get('capacity'))
            except ValueError:
                selected_capacity = None
        elif self.instance.pk:
            selected_capacity = self.instance.capacity
        else:
            selected_capacity = None

        if selected_capacity:
            self.fields['table'].queryset = Table.objects.filter(capacity=selected_capacity, status='available')
        else:
            self.fields['table'].queryset = Table.objects.none() #no tables if no capacity is selected

        #get the opening hours for the selected day 
        if 'date' in self.data:
            selected_date = self.data.get('date')
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