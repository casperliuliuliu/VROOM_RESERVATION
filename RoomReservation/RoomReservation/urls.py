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
from django.contrib import admin
from django.urls import path, include
from reservation import views as reservation_views, feeds as reservation_feeds
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("room.urls")),
    path('reservation/', include("reservation.urls")),
    path('attendee/<str:id>', reservation_views.attendance, name="attendance"),
    path('accounts/', include("account.urls")),
    path("attendee/<str:id>/ical", reservation_feeds.AttendeeFeed(), name="attendee_feed"),
    path("<str:model>/<str:id>/gcal", reservation_views.google_calendar_auth, name="google_calendar_link"),
    path('calendar/redirect', reservation_views.google_calendar_callback, name="google_calendar_callback"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
