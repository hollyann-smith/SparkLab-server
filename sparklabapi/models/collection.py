from django.db import models

from sparklabapi.models.idea import Idea
from sparklabapi.models.user import User

class Collection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    cover = models.CharField(max_length=200)
    ideas = models.ManyToManyField(Idea, related_name='ideas')
