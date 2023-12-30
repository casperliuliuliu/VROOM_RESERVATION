from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from reservation.forms import AttendeeForm
from .models import Reservation, Attendee

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
    if(reservation.user != request.user):
        return HttpResponse('Unauthorized Access to this reservation', status=401)
    attendees = Attendee.objects.filter(reservation=reservation).all()
    return render(request, 'reservation/show.html', {
        'reservation': reservation,
        'attendees': attendees
    })
    
@login_required
def add_attendee(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    if(reservation.user != request.user):
        return HttpResponse('Unauthorized Access to this reservation', status=401)
    
    if request.method == 'POST':
        return add_attendee_post(request, reservation)
    
    return render(request, 'reservation/attendee/add.html', {
        'reservation': reservation,
        'form': AttendeeForm()
    })

def add_attendee_post(request, reservation):
    form = AttendeeForm(request.POST)
    if not form.is_valid():
        return render(request, 'reservation/attendee/add.html', {
            'reservation': reservation,
            'form': form
        })
    
    attendee = form.save(commit=False)
    other_attendee = Attendee.objects.filter(reservation=reservation, email=attendee.email).first()
    if(other_attendee):
        messages.error(request, 'Email address is already associated with this reservation. Please remove the attendee with the identical email before adding it back again!', extra_tags='danger')
        return render(request, 'reservation/attendee/add.html', {
            'reservation': reservation,
            'form': form
        }
    )
    attendee.reservation = reservation
    attendee.save()
    messages.success(request, 'Attendee added successfully', extra_tags='success')
    return redirect('reservation_show', reservation.id)

@login_required
def attendee_show(request, reservation_id, attendee_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    if(reservation.user != request.user):
        return HttpResponse('Unauthorized Access to this reservation', status=401)
    
    attendee = get_object_or_404(Attendee, id=attendee_id)
    if(attendee.reservation != reservation):
        return HttpResponse('Unauthorized Access to this attendee', status=401)
    
    return render(request, 'reservation/attendee/show.html', {
        'reservation': reservation,
        'attendee': attendee
    })