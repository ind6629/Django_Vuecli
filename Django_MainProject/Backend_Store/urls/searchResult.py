from django.urls import path
from ..views.searchResult import load



urlpatterns = [
    path('result', load, name="searchResult_load"),
]