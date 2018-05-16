from django.urls import path, include

from . import views

urlpatterns = [
    path('friends', views.friend_list, name='friend_list'),
    path('viewrequest', views.view_friend_request, name='view_friend_request'),
    path('', include('settings.urls')),
]
