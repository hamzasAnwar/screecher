from django.urls import path

from . import views

urlpatterns = [
    path('', views.ad_service, name='ad_service'),
    path('counter', views.ad_count, name='ad_count'),
    path('banner', views.banner, name='banner'),
]
