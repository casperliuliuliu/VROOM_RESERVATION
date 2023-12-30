from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Reservation

# Create your views here.
@login_required
def index(request):
    reservations = Reservation.objects.filter(user=request.user)
    return render(request, 'reservation/index.html', {
        'reservations': reservations
    })

@login_required
def show(request, id):
    reservation = get_object_or_404(Reservation, id=id)
    return render(request, 'reservation/index.html', {
        'reservation': reservation
    })
    