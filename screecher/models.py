from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE, default=None)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    username = models.CharField(max_length=30)
    email = models.CharField(max_length=30)


class Screech(models.Model):
    user = models.ForeignKey(User, on_delete=None)
    content = models.TextField()
    num_of_comments = models.IntegerField(default=0)
    date = models.DateField(auto_now_add=True)
