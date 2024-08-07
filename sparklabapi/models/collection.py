from django.db import models

from sparklabapi.models.user import User

class Collection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    cover = models.CharField()
