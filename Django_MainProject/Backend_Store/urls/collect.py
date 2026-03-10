from django.urls import path
from ..views.collect import load
from ..views.collect import remove
from ..views.collect import collections
from ..views.collect import checkCollect
from ..views.collect import collect

urlpatterns = [
    path('collection', load, name="collect_load"),
    path('api/removeCollection', remove, name="collect_remove"),
    path('api/checkCollect', checkCollect, name="collect_checkCollect"),
    path('api/collect', collect, name="collect_collect"),
    path('api/collections/<int:userId>', collections, name="collect_collections")
]