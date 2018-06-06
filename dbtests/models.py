from django.db import models


class Feedback(models.Model):
    username = models.TextField()
    content = models.TextField(null=True)
    date = models.DateField(auto_now_add=True, null=True)
