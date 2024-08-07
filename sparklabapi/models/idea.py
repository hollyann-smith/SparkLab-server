from django.db import models

from sparklabapi.models.supply import Supply
from sparklabapi.models.user import User

class Idea(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.CharField()
    saved = models.BooleanField()
    img = models.CharField()
    supply = models.ManyToManyField(Supply)
