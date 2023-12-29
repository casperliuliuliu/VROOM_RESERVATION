from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Room
from .forms import ReservationForm 
from reservation.models import Reservation

# Create your views here.
def index(request):
    rooms = Room.objects.all()
    return render(request, 'room/index.html',{
        'rooms': rooms
    })
    
def show(request, id):
    room = get_object_or_404(Room, id=id)
    return render(request, 'room/show.html', {
        'room': room
    })
    
@login_required
def reserve(request, id):
    if request.method == 'POST':
        return reserve_post(request, id)
        
    room = get_object_or_404(Room, id=id)
    return render(request, 'room/reserve.html', {
        'room': room,
        'form': ReservationForm()
    })


def reserve_post(request, id):
    room = get_object_or_404(Room, id=id)
    form = ReservationForm(request.POST)
    if not form.is_valid():
        return render(request, 'room/reserve.html', {
            'room': room,
            'form': form
        })
    
    reservation = Reservation.objects.create(**form.cleaned_data, room=room, user=request.user)
    return redirect('reservation_show', id=reservation.id)
        