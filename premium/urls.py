from django.urls import path, include

from . import views

urlpatterns = [
    path('premium', views.premium_area, name='premium'),
    path('', include('friendship.urls')),
]
