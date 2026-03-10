from django.urls import path
from ..views.buy import add_to_cart 
from ..views.buy import cart 
from ..views.buy import remove_from_cart 
from ..views.buy import add_to_order 
from ..views.buy import checkout 

urlpatterns = [
    path('api/add_to_cart', add_to_cart, name="buy_add_to_cart"),
    path('api/add_to_order', add_to_order, name="buy_add_to_order"),
    path('api/carts/<int:userId>', cart, name="buy_cart"),
    path('api/checkout', checkout, name="buy_checkout"),
    path('remove_from_cart/<int:cart_id>', remove_from_cart, name="buy_remove_from_cart")
]