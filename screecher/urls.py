from django.urls import path

from . import views_user
from . import views_screeches
from . import views_messages

urlpatterns = [
    # Screeches related urls
    path('', views_screeches.index, name='index'),
    path('screech', views_screeches.screech, name='screech'),
    path('messages', views_messages.messages, name='messages'),
    # User management related urls
    path('login', views_user.login_view, name='login'),
    path('logout', views_user.logout_view, name='logout'),
    path('register', views_user.registration, name='registration'),
    path('profile/<int:profile_id>', views_user.profile, name='profile'),
]
