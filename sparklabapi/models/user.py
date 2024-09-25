from django.db import models

class User(models.Model):
    username = models.CharField(max_length=500)
    uid = models.CharField(max_length=50)
