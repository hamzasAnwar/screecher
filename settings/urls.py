from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('settings', views.settings_page, name='settings'),
    path('change-user', views.change_profile, name='change_profile'),
    path('track', views.tracking, name='tracking'),
    path('log', views.logging, name='logging'),
    path('', include('screecher.urls')),
]
