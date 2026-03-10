from django.urls import path
from ..views.realtime_analysis import init
from ..views.realtime_analysis import clickData
from ..views.realtime_analysis import searchData
from ..views.realtime_analysis import cartData
from ..views.realtime_analysis import orderData
from ..views.realtime_analysis import otherData


urlpatterns = [
    path('realtime_analysis', init, name="realtime_analysis_init"),
    path('realtime_clickData', clickData, name="realtime_analysis_clickData"),
    path('realtime_searchData', searchData, name="realtime_analysis_searchData"),
    path('realtime_cartData', cartData, name="realtime_analysis_cartData"),
    path('realtime_orderData', orderData, name="realtime_analysis_orderData"),
    path('realtime_otherData', otherData, name="realtime_analysis_otherData"),
]