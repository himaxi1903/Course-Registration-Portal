from django.conf.urls import url
from django.urls import path
from django.urls import include
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'myapp/', include('myapp.urls')),
]
