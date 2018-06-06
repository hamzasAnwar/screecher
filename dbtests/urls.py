from django.urls import path, include

from . import views

urlpatterns = [
    path('search', views.profile_search, name='profile_search'),
    path('feedback', views.feedback, name='feedback'),
    path('save-feedback', views.save_feedback, name='save_feedback'),
    path('', include('premium.urls')),
]

