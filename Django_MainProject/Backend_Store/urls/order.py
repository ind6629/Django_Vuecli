from django.urls import path
from ..views.order import load
from ..views.order import cancelOrder
from ..views.order import settleOrder
from ..views.order import order


urlpatterns = [
    path('order', load, name="order_load"),
    path('cancelOrder', cancelOrder, name="order_cancelOrder"),
    path('settleOrder', settleOrder, name="order_settleOrder"),
    path('api/orders/<int:userId>', order, name="order_order"),
]