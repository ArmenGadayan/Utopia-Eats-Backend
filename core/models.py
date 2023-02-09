from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True) 
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    height_feet = models.IntegerField(null=True, blank=True)
    height_inches = models.IntegerField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)