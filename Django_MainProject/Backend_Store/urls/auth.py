from django.urls import path
from ..views.auth import login 
from ..views.auth import register 
from ..views.auth import logout
from ..views.auth import checkLogin
from ..views.auth import update_profile 
from ..views.auth import csrf_token_view 

urlpatterns = [
    path('api/login', login, name="auth_login"),
    path('api/register', register, name="auth_register"),
    path('api/logout', logout, name="auth_logout"),
    path('api/checkLogin', checkLogin, name="auth_checkLogin"),
    path('api/update_profile', update_profile, name="auth_update_profile"),
    path('api/csrf_token/', csrf_token_view, name='csrf_token')
]