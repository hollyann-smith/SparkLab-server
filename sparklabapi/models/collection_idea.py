from django.db import models

from sparklabapi.models.collection import Collection
from sparklabapi.models.idea import Idea

class CollectionIdea(models.Model):
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE)
