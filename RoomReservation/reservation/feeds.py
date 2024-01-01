from RoomReservation import settings
from django_ical.views import ICalFeed
from .models import Reservation, Attendee
from datetime import datetime

class ReservationFeed(ICalFeed):
    """
    A simple event calender
    """
    reservation_id = None
    product_id = 'Best Event Manager'
    timezone = 'Asia/Taipei'
    event_name = None
    

    file_name = 'feed.ics'

    def get_object(self, request, *args, **kwargs):
        reservation_id = kwargs.get("id")
        return reservation_id 

    def items(self, reservation_id):
        reservation = Reservation.objects.filter(id = reservation_id).all()
        return reservation

    def item_title(self, item):
        return item.event_name

    def item_start_datetime(self, item):
        start_datetime = datetime.combine(item.start_date, item.start_time)
        return start_datetime
    
    def item_end_datetime(self, item):
        end_datetime = datetime.combine(item.start_date, item.end_time())
        return end_datetime
    
    def item_location(self, item):
        return f"{item.room.name} - {item.room.location}"
    
    def item_link(self, item):
        return f"{settings.DEFAULT_HOST}/reservation/{item.id}"
    
class AttendeeFeed(ICalFeed):
    """
    A simple event calender
    """
    reservation_id = None
    product_id = 'Best Event Manager'
    timezone = 'Asia/Taipei'
    event_name = None
    file_name = 'feed.ics'

    def get_object(self, request, *args, **kwargs):
        attendee_id = kwargs.get("id")
        attendee = Attendee.objects.filter(id = attendee_id).first()
        reservation_id = attendee.reservation.id
        return reservation_id 

    def items(self, reservation_id):
        reservation = Reservation.objects.filter(id = reservation_id).all()
        return reservation

    def item_title(self, item):
        return item.event_name

    def item_start_datetime(self, item):
        start_datetime = datetime.combine(item.start_date, item.start_time)
        return start_datetime
    
    def item_end_datetime(self, item):
        end_datetime = datetime.combine(item.start_date, item.end_time())
        return end_datetime
    
    def item_location(self, item):
        return f"{item.room.name} - {item.room.location}"
    
    def item_link(self, item):
        return f"{settings.DEFAULT_HOST}/attendee/{item.id}"