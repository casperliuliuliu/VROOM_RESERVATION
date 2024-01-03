from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class MeetingRoomFacility(models.Model):
    name = models.CharField(max_length=50)
    icon = models.CharField(max_length=50, null=True, blank=True)
    
    def __str__(self):
        return f"{self.name}"

class Room(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    capacity = models.IntegerField()
    size = models.FloatField()
    location = models.TextField()
    price_per_hour = models.IntegerField()
    image = models.ImageField(upload_to='rooms/', null=True, blank=True)
    facilities = models.ManyToManyField(MeetingRoomFacility, related_name='rooms')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rooms')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"
    
