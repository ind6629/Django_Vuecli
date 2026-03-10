from django.urls import path
from ..views.recommend import recommend


urlpatterns = [
    path('api/recommend', recommend, name="recommend"),
]