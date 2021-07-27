from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls import url
from django.views.static import serve

urlpatterns = [
    path('admincbv2/', admin.site.urls),
    path('auth/',include('usermanager.urls')),
    path('',include('blogAPP.urls')),
    url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT})
]
