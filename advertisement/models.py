from django.db import models


class Advertisement(models.Model):
    token = models.CharField(default="", max_length=64)
    host = models.CharField(default="", max_length=64)
    loaded = models.IntegerField(default=0)
