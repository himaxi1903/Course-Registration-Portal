from django.conf.urls.static import static
from django.urls import path
from myapp import views
from django.conf import settings


app_name = 'myapp'

urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'about/', views.about, name='about'),
    path(r'<int:topic_id>/', views.detail, name='topic_detail'),
    path(r'findcourses/', views.findcourses, name='findcourses'),
    path(r'place_order/', views.place_order, name='place_order'),
    path(r'review/', views.review, name='review'),
    path(r'login/', views.user_login, name='login'),
    path(r'logout/', views.user_logout, name='logout'),
    path(r'myaccount', views.myaccount, name='myaccount'),
    path(r'register/', views.register, name='register'),
    path(r'myorders/', views.myorders, name='myorders'),
    path(r'forgot_password/', views.forgot_password, name='forgot_password')
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
