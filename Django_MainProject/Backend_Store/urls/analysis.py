from django.urls import path
from ..views.analysis import init 
from ..views.analysis import realtime_init 
from ..views.analysis import clickData 
from ..views.analysis import searchData 
from ..views.analysis import cartData 
from ..views.analysis import orderData 
from ..views.analysis import otherData 
from ..views.analysis import realtime_clickData 
from ..views.analysis import realtime_searchData 
from ..views.analysis import realtime_cartData 
from ..views.analysis import realtime_orderData 

urlpatterns = [
    path('analysis', init, name="analysis_init"),
    path('realtime_analysis', realtime_init, name="analysis_realtime_init"),
    path('api/clickData', clickData, name="analysis_clickData"),
    path('api/searchData', searchData, name="analysis_searchData"),
    path('api/cartData', cartData, name="analysis_cartData"),
    path('api/orderData', orderData, name="analysis_orderData"),
    path('api/otherData', otherData, name="analysis_otherData"),
    path('api/realtime_clickData', realtime_clickData, name="analysis_realtime_clickData"),
    path('api/realtime_searchData', realtime_searchData, name="analysis_realtime_searchData"),
    path('api/realtime_cartData', realtime_cartData, name="analysis_realtime_cartData"),
    path('api/realtime_orderData', realtime_orderData, name="analysis_realtime_orderData"),
]