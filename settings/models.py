from django.contrib.auth.models import User
from django.db import models


class PageLog(models.Model):
    user = models.ForeignKey(User, on_delete=None)
    page = models.TextField()
    date = models.DateField(auto_now_add=True)
