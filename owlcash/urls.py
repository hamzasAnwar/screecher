from django.urls import path, include

from . import views

urlpatterns = [
    path('cash', views.miner_page, name='miner'),
    path('cash/store', views.store_wallet, name='store_cash'),
    path('cash/wallet', views.get_wallet, name='wallet'),
    path('', include('dbtests.urls')),
]
