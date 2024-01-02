from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from django.contrib import messages
from django.conf import settings
from .models import Room
from .forms import ReservationForm, RoomForm 
from reservation.models import Reservation
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.http import JsonResponse
from django.utils.dateparse import parse_datetime
from datetime import datetime


# Create your views here.
def index(request):
    rooms = Room.objects.all()
    return render(request, 'room/index.html',{
        'rooms': rooms
    })
    
def show(request, id):
    room = get_object_or_404(Room, id=id)
    
    try:
        type = request.GET["type"]
    except:
        type = None

    if type == 'calendar':
        return show_calendar(request, room)

    return render(request, 'room/show.html', {
        'room': room
    })

def show_calendar(request, room):
    try:
        start = request.GET["start"]
        end = request.GET["end"]
    except:
        start = None
        end = None

    if not start and not end:
        return JsonResponse({'error': 'start and end time are required'}, status=400)
    
    start_date = parse_datetime(start).date()
    end_date = parse_datetime(end).date()
    
    reservations = Reservation.objects.filter(room=room, start_date__gte=start_date, start_date__lte=end_date).all()

    events_data = []

    for reservation in reservations:
        event_data = {
            'title': reservation.event_name,
            'start': datetime.combine(reservation.start_date, reservation.start_time).isoformat(),
            'end': datetime.combine(reservation.start_date, reservation.end_time()).isoformat(),
        }
        events_data.append(event_data)
    return JsonResponse(events_data, safe=False)
    
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
    reservation = form.save(commit=False)

    endtime = reservation.end_time()
    other_reservation = Reservation.objects.raw("""
        SELECT *, TIME(TIME(start_time, duration || ' hours'), '-1 seconds')
        FROM reservation_reservation
        WHERE 
            room_id = %s AND 
            start_date = %s AND 
            (
                start_time < %s AND
                TIME(TIME(start_time, duration || ' hours'), '-1 seconds') >= %s
            )
        LIMIT 1""", 
        [room.id, reservation.start_date, endtime, reservation.start_time])
    
    if(len(other_reservation) > 0):
        messages.error(request, 'This room is already reserved for this time', extra_tags='danger')
        return render(request, 'room/reserve.html', {
            'room': room,
            'form': form
        })
    reservation = Reservation.objects.create(**form.cleaned_data, room=room, user=request.user)
    
    messages.success(request, 'Reservation created successfully', extra_tags='success')

    redirect_link = f'{settings.DEFAULT_HOST}/reservation/{reservation.id}'
    subject = f'[{reservation.event_name}]Meeting Room Reservation Confirmation'
    html_message = render_to_string('emails/reservation.html', {'reservation': reservation, 'redirect_link': redirect_link})
    plain_message = strip_tags(html_message)
    from_email = 'Best Reservation Website <sandboxatrest@gmail.com>'
    to = reservation.user.email 

    mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)

    return redirect('reservation_show', id=reservation.id)
        
@staff_member_required
def add(request):
    if request.method == 'POST':
        return add_post(request)
        
    return render(request, 'room/add.html', {
        'form': RoomForm()
    })


def add_post(request):
    form = RoomForm(request.POST, request.FILES)
    if not form.is_valid():
        return render(request, 'room/add.html', {
            'form': form
        })
    room = form.save(commit=False)
    room.created_by = request.user
    room.save()
    form.save_m2m()
    messages.success(request, 'New room added successfully', extra_tags='success')
    return redirect('room_show', id=room.id)

@staff_member_required
def edit(request, id):
    room = get_object_or_404(Room, id=id)
    if request.method == 'POST':
        return edit_post(request, room)
        
    return render(request, 'room/edit.html', {
        'room': room,
        'form': RoomForm(instance=room)
    })

def edit_post(request, room):
    form = RoomForm(request.POST, request.FILES, instance=room)
    if not form.is_valid():
        return render(request, 'room/add.html', {
            'form': form
        })
    old_image = room.image
    room = form.save(commit=False)
    if room.image:
        room.image = old_image
    
    room.save()
    form.save_m2m()

    messages.success(request, 'Room info updated', extra_tags='success')
    return redirect('room_show', id=room.id)

@staff_member_required
def delete_post(request, id):
    room = get_object_or_404(Room, id=id)
    try:
        action = request.POST["action"]
    except:
        action = None
    if action != 'delete':
        return redirect('room_show', id=room.id)
    room.delete()
    messages.success(request, 'Room deleted', extra_tags='success')
    return redirect('room_index')