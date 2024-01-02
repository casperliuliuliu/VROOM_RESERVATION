from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, time
import uuid

# Create your models here.
class Reservation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event_name = models.CharField(max_length=225)
    room = models.ForeignKey('room.Room', on_delete=models.CASCADE, related_name='reservations')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    start_time = models.TimeField()
    duration = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    canceled_at = models.DateTimeField(null=True, blank=True)

    def end_time(self):
        return time(hour=self.start_time.hour + self.duration - 1 , minute=59, second=59 )
    
    def cancel(self):
        self.canceled_at = models.DateTimeField(null=True, blank=True, auto_now = True)

    class ReservationStatus(models.TextChoices):
        COMPLETED = 'Completed'
        CANCELED = 'Canceled'
        ONGOING = 'On Going'
        SCHEDULED = 'Scheduled'

    def status(self):
        if self.canceled_at:
            return self.ReservationStatus.CANCELED
        
        print(datetime.now().date(), self.start_date, datetime.now().time(), self.end_time())
        if datetime.now().date() > self.start_date or (datetime.now().date() >= self.start_date and datetime.now().time() > self.end_time()):
            return self.ReservationStatus.COMPLETED
        if datetime.now().date() < self.start_date or (datetime.now().date() <= self.start_date and datetime.now().time() < self.start_time):
            return self.ReservationStatus.SCHEDULED
        return self.ReservationStatus.ONGOING


    def __str__(self):
        return f"{self.event_name}"
    
class Attendee(models.Model):
    class ResponseStatus(models.TextChoices):
        ACCEPTED = 'ACCEPTED'
        DECLINED = 'DECLINED'
        WAITING = 'WAITING'
        
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=225)
    email = models.EmailField()
    response_status = models.CharField(max_length=50, choices=ResponseStatus.choices, default=ResponseStatus.WAITING)
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['reservation', 'email']
        
    def __str__(self):
        return f"{self.name} - {self.email}"
    
    