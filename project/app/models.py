from django.db import models
from project.settings import ADDRESS_MAX_LENGTH

class Place(models.Model):
    raw_address = models.CharField(max_length=ADDRESS_MAX_LENGTH)
    formatted_address = models.CharField(max_length=ADDRESS_MAX_LENGTH)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
