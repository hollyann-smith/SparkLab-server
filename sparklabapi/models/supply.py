from django.db import models


class Supply(models.Model):
    name = models.CharField(max_length=30)
