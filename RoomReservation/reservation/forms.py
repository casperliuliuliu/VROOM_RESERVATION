from django import forms
from reservation.models import Attendee

class AttendeeForm(forms.ModelForm):
    name = forms.CharField(label='Name', max_length=225, required=True, 
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email', required=True,
                                 widget=forms.EmailInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = Attendee
        fields = ['name', 'email']