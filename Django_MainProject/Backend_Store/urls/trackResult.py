from django.urls import path
from ..views.trackResult import track_result



urlpatterns = [
    path('api/trackResult', track_result, name="trackResult_track_result"),
]