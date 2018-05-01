from django.urls import path

from . import views

urlpatterns = [
    path('user/<profile_id>', views.user_info, name='user'),
]
