from django.urls import path

from . import views

urlpatterns = [
    path('user/<int:profile_id>', views.user_info, name='user'),
]
