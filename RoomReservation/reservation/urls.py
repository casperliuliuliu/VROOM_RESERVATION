"""
URL configuration for RoomReservation project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views
from .feeds import ReservationFeed

urlpatterns = [
    path("", views.index, name="reservation_index"),
    path("<str:id>", views.show, name="reservation_show"),
    path("<str:id>/extend", views.extend, name="reservation_extend"),
    path("<str:reservation_id>/attendee", views.add_attendee, name="reservation_attendee_add"), 
    path("<str:reservation_id>/attendee/<str:attendee_id>", views.attendee_show, name="reservation_attendee_show"), 
    path("<str:id>/ical", ReservationFeed(), name="reservation_feed"),
    # path("<str:id>/gcal", views.google_calendar_auth, name="reservation_google_calendar"),
]
