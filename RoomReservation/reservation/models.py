from django.db import models
from django.contrib.auth.models import User

import uuid

# Create your models here.
class Reservation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event_name = models.CharField(max_length=225)
    room = models.ForeignKey('room.Room', on_delete=models.CASCADE, related_name='reservations')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    canceled_at = models.DateTimeField(null=True, blank=True)
    
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
    
    