from django.db import models

class User(models.Model):
    username = models.CharField(max_length=200)
    uid = models.CharField(max_length=50)
