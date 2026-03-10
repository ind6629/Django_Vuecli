"""
URL configuration for Django_MainProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("Backend_Store/", include("Backend_Store.urls.analysis")),
    path("Backend_Store/", include("Backend_Store.urls.auth")),
    path("Backend_Store/", include("Backend_Store.urls.buy")),
    path("Backend_Store/", include("Backend_Store.urls.collect")),
    path("Backend_Store/", include("Backend_Store.urls.comments")),
    path("Backend_Store/", include("Backend_Store.urls.main")),
    path("Backend_Store/", include("Backend_Store.urls.order")),
    path("Backend_Store/", include("Backend_Store.urls.realtime_analysis")),
    path("Backend_Store/", include("Backend_Store.urls.searchResult")),
    path("Backend_Store/", include("Backend_Store.urls.track")),
    path("Backend_Store/", include("Backend_Store.urls.trackResult")),
    path("Backend_Store/", include("Backend_Store.urls.recommend")),
    path('',TemplateView.as_view(template_name="index.html"))
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
