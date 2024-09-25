from django.db import models

from sparklabapi.models.supply import Supply
from sparklabapi.models.user import User

class Idea(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=800)
    description = models.CharField(max_length=800)
    saved = models.BooleanField()
    img = models.URLField(max_length=800)
    supplies = models.ManyToManyField(Supply, related_name='ideas')
