from django.urls import path
from ..views.track import track_event



urlpatterns = [
    path('api/tracking', track_event, name="track_track_event"),
]