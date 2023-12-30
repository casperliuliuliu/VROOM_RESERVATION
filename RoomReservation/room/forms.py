from django import forms
from reservation.models import Reservation

class ReservationForm(forms.ModelForm):
    event_name = forms.CharField(label='Event Name', max_length=225, required=True, 
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))
    start_date = forms.DateField(label='Date', required=True,
                                 widget=forms.DateInput(attrs={'class': 'form-control datepicker'}))
    start_time = forms.TimeField(label='Start Time',required=True,
                                 widget=forms.TimeInput(attrs={'class': 'form-control timepicker'}))
    duration = forms.IntegerField(label='Duration', required=True, 
                                  widget=forms.NumberInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = Reservation
        fields = ['event_name', 'start_date', 'start_time', 'duration']