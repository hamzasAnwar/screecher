from django.contrib.auth.models import User
from django.db import models


class OwlCash(models.Model):
    user = models.ForeignKey(User, on_delete=None)
    hash = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
