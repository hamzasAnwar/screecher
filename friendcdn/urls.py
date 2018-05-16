from django.urls import path, include

from . import views

urlpatterns = [
    path('addfriend', views.add_friend, name='add_friend'),
    path('requestfriend', views.add_request_friend, name='request_friend'),
    path('acceptfriend', views.accept_requested_friend, name='accept_friend'),
    path('friendscript', views.friend_script, name='friend_script'),
    path('', include('cdn.urls')),
]
