from django import forms
from reservation.models import Reservation
from room.models import Room, MeetingRoomFacility

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

class RoomForm(forms.ModelForm):
    name = forms.CharField(label='Name', max_length=225, required=True,
                                    widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(label='Description', required=False,
                                    widget=forms.Textarea(attrs={'class': 'form-control'}))
    capacity = forms.IntegerField(label='Capacity', required=True,
                                    widget=forms.NumberInput(attrs={'class': 'form-control'}))
    size = forms.IntegerField(label='Size', required=True,
                                    widget=forms.NumberInput(attrs={'class': 'form-control'}))
    location = forms.CharField(label='Location', max_length=225, required=True,
                                    widget=forms.TextInput(attrs={'class': 'form-control'}))
    price_per_hour = forms.IntegerField(label='Price Per Hour', required=True,
                                    widget=forms.NumberInput(attrs={'class': 'form-control'}))
    image = forms.ImageField(label='Image', required=False,
                                    widget=forms.FileInput(attrs={'class': 'form-control'}))
    facilities = forms.ModelMultipleChoiceField(label='Facilities', required=False, queryset=MeetingRoomFacility.objects.order_by("name").all(),
                                    widget=forms.CheckboxSelectMultiple())
    
    class Meta:
        model = Room
        fields = ['name', 'description', 'capacity', 'size', 'location', 'price_per_hour', 'image', 'facilities']