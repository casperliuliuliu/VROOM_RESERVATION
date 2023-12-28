from django.shortcuts import render
from .models import Room
from django.shortcuts import render, get_object_or_404
from .models import Room

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

