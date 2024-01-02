from django.conf import settings
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from django.conf import settings
from datetime import datetime

from reservation.forms import AttendeeForm
from .models import Reservation, Attendee
import os

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from django.http import JsonResponse
from django.utils.dateparse import parse_datetime
from django.shortcuts import redirect

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'



CLIENT_SECRETS_FILE = "credentials.json"

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection and REDIRECT URL.
SCOPES = ['https://www.googleapis.com/auth/calendar']

REDIRECT_URL = settings.DEFAULT_HOST + '/calendar/redirect'
API_SERVICE_NAME = 'calendar'
API_VERSION = 'v3'

# @login_required
def google_calendar_auth(request, id, model):
    if model not in ('reservation', 'attendee'):
        return HttpResponse('Invalid request', status=400)
    
    flow = Flow.from_client_secrets_file(
        'client_secret.json',
        scopes=['https://www.googleapis.com/auth/calendar'],
        redirect_uri=REDIRECT_URL)

    authorization_url, state = flow.authorization_url()

    request.session['model'] = model
    request.session['model_id'] = id
    request.session['state'] = state

    return redirect(authorization_url)

def google_calendar_callback(request):
    # Retrieve data from the session
    model = request.session.get('model')
    model_id = request.session.get('model_id')
    del request.session['model']
    del request.session['model_id']
    if(model_id == None):
        return HttpResponse('Invalid request', status=400)
    
    if model == 'reservation':
        reservation = Reservation.objects.filter(id=model_id).first()
        if(reservation == None):
            return HttpResponse('Invalid request', status=400)
    
    if model == 'attendee':
        attendee = Attendee.objects.filter(id=model_id).first()
        if(attendee == None):
            return HttpResponse('Invalid request', status=400)
        reservation = attendee.reservation

    state = request.session['state']
    if state is None:
        return HttpResponse("State parameter missing.", status=400)

    flow = Flow.from_client_secrets_file(
        'client_secret.json', scopes=SCOPES, state=state)
    flow.redirect_uri = REDIRECT_URL

    # Use the authorization server's response to fetch the OAuth 2.0 tokens.
    authorization_response = request.get_full_path()
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials
    request.session['credentials'] = credentials_to_dict(credentials)

    if 'credentials' not in request.session:
        return redirect('v1/calendar/init')

    credentials = Credentials(
        **request.session['credentials'])

    # Use the Google API Discovery Service to build client libraries, IDE plugins,
    # and other tools that interact with Google APIs.
    # The Discovery API provides a list of Google APIs and a machine-readable "Discovery Document" for each API
    service = build(
        API_SERVICE_NAME, API_VERSION, credentials=credentials)

    # Define your event
    event = {
        'summary': reservation.event_name,
        'start': {
            'dateTime': datetime.combine(reservation.start_date, reservation.start_time).isoformat(),
            'timeZone': settings.TIME_ZONE,
        },
        'end': {
            'dateTime': datetime.combine(reservation.start_date, reservation.end_time()).isoformat(),
            'timeZone': settings.TIME_ZONE,
        },
    }

    # Add the event
    event = service.events().insert(calendarId='primary', body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))

    messages.success(request, 'Event added successfully to your Google Calendar', extra_tags='success')
    
    if model == 'reservation':
        return redirect('reservation_show', reservation.id)
    if model == 'attendee':
        return redirect('attendance', attendee.id)
    
    return HttpResponse('Invalid request', status=400)

def credentials_to_dict(credentials):
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}

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
    
    try:
        type = request.GET["type"]
    except:
        type = None

    if type == 'calendar':
        return show_calendar(request, reservation)

    if(reservation.user != request.user):
        return HttpResponse('Unauthorized Access to this reservation', status=401)
    attendees = Attendee.objects.filter(reservation=reservation).all()
    return render(request, 'reservation/show.html', {
        'reservation': reservation,
        'attendees': attendees
    })

def show_calendar(request, reservation):
  
    event_data = [{
        'title': reservation.event_name,
        'start': datetime.combine(reservation.start_date, reservation.start_time).isoformat(),
        'end': datetime.combine(reservation.start_date, reservation.end_time()).isoformat(),
    }]
    return JsonResponse(event_data, safe=False)
    
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
def cancel_reservation(request, reservation_id):
    print('hello ==========')
    reservation = get_object_or_404(Reservation, id=reservation_id)
    print(reservation.canceled_at)
    reservation.cancel()
    print(reservation.canceled_at)
    print(reservation.status())

    return render(request, 'reservation/show.html', {
        'reservation': reservation,
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
    
    try:
        type = request.GET["type"]
    except:
        type = None

    if type == 'calendar':
        return attendance_show_calendar(request, reservation)

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

def attendance_show_calendar(request, reservation):
  
    event_data = [{
        'title': reservation.event_name,
        'start': datetime.combine(reservation.start_date, reservation.start_time).isoformat(),
        'end': datetime.combine(reservation.start_date, reservation.end_time()).isoformat(),
    }]
    return JsonResponse(event_data, safe=False)

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