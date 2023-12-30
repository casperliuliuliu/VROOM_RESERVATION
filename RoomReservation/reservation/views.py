from django.conf import settings
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

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
    
    redirect_link = f'{settings.DEFAULT_HOST}/attendee/{attendee.id}'
    subject = f'Invitation to [{reservation.event_name}]'
    html_message = render_to_string('emails/attendee.html', {'reservation': reservation, 'attendee': attendee, 'redirect_link': redirect_link})
    plain_message = strip_tags(html_message)
    from_email = 'Best Reservation Website <sandboxatrest@gmail.com>'
    to = attendee.email 

    mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)

    return redirect('reservation_show', reservation.id)

@login_required
def attendee_show(request, reservation_id, attendee_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    if(reservation.user != request.user):
        return HttpResponse('Unauthorized Access to this reservation', status=401)
    
    attendee = get_object_or_404(Attendee, id=attendee_id)
    if(attendee.reservation != reservation):
        return HttpResponse('Unauthorized Access to this attendee', status=401)
    
    if request.method == 'POST':
        return attendee_show_post(request, reservation, attendee)
    
    return render(request, 'reservation/attendee/show.html', {
        'reservation': reservation,
        'attendee': attendee
    })

@login_required
def attendee_show_post(request, reservation, attendee):
    if request.POST["action"] == 'resend_invitation':
        redirect_link = f'{settings.DEFAULT_HOST}/attendee/{attendee.id}'
        subject = f'Invitation to [{reservation.event_name}]'
        html_message = render_to_string('emails/attendee.html', {'reservation': reservation, 'attendee': attendee, 'redirect_link': redirect_link})
        plain_message = strip_tags(html_message)
        from_email = 'Best Reservation Website <sandboxatrest@gmail.com>'
        to = attendee.email 
        mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
        messages.success(request, 'Invitation has been resent successfully', extra_tags='success')
        return redirect('reservation_attendee_show', reservation_id = reservation.id, attendee_id = attendee.id)
    elif request.POST["action"] == 'cancel_invitation':
        if request.POST["send_canceled_email"] == "true":
            subject = f'Cancellation of [{reservation.event_name}]'
            html_message = render_to_string('emails/canceled.html', {'reservation': reservation, 'attendee': attendee})
            plain_message = strip_tags(html_message)
            from_email = 'Best Reservation Website <sandboxatrest@gmail.com>'
            to = attendee.email 
        else:
            subject = f'Change in Meeting Attendance for [{reservation.event_name}]'
            html_message = render_to_string('emails/attendee_removed.html', {'reservation': reservation, 'attendee': attendee})
            plain_message = strip_tags(html_message)
            from_email = 'Best Reservation Website <sandboxatrest@gmail.com>'
            to = attendee.email 
        mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
        messages.success(request, f'Invitation to {attendee.name} canceled successfully', extra_tags='success')
        attendee.delete()

        return redirect('reservation_show', id = reservation.id)
    else:
        return HttpResponse('Invalid action', status=400)
    
def attendance(request, id):
    attendee = get_object_or_404(Attendee, id=id)
    reservation = attendee.reservation
    if request.method == 'POST':
        return attendance_post(request, attendee, reservation)
    if attendee.response_status == attendee.ResponseStatus.WAITING:
        return render(request, 'attendee/confirm.html', {
        'attendee': attendee,
        'reservation': reservation
    })
    if attendee.response_status == attendee.ResponseStatus.ACCEPTED:
        return render(request, 'attendee/show.html', {
            'attendee': attendee,
            'reservation': reservation
        })
    if attendee.response_status == attendee.ResponseStatus.DECLINED:
        return render(request, 'attendee/declined.html', {
            'attendee': attendee,
            'reservation': reservation
        })

def attendance_post(request, attendee, reservation):
    if attendee.response_status != attendee.ResponseStatus.WAITING:
        return HttpResponse('Invalid action', status=400)
    
    if request.POST["action"] == 'accept_invitation':
        attendee.response_status = attendee.ResponseStatus.ACCEPTED
        attendee.save()
        messages.success(request, 'Attendance confirmed successfully', extra_tags='success')
        return redirect('attendance', id = attendee.id)
    elif request.POST["action"] == 'decline_invitation':
        attendee.response_status = attendee.ResponseStatus.DECLINED
        attendee.save()
        messages.success(request, 'Attendance declined successfully', extra_tags='success')
        return redirect('attendance', id = attendee.id)
    else:
        return HttpResponse('Invalid action', status=400)