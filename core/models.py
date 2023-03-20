from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ACTIVITY_LEVEL_LOW = 1.2
    ACTIVITY_LEVEL_MODERATE = 1.55
    ACTIVITY_LEVEL_HIGH = 1.9
    ACTIVITY_LEVEL_CHOICES = [
        (ACTIVITY_LEVEL_LOW, "Low"),
        (ACTIVITY_LEVEL_MODERATE, "Moderate"),
        (ACTIVITY_LEVEL_HIGH, "High")
    ]

    GOAL_LOSE = "Lose"
    GOAL_MAINTAIN = "Maintain"
    GOAL_GAIN = "Gain"

    GOAL_CHOICES = [
        (GOAL_LOSE, "Lose"),
        (GOAL_MAINTAIN, "Maintain"),
        (GOAL_GAIN, "Gain")
    ]


    email = models.EmailField(unique=True) 
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    height_feet = models.IntegerField(null=True, blank=True)
    height_inches = models.IntegerField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    bmr = models.FloatField(null=True, blank=True)
    activity_level = models.FloatField(default=ACTIVITY_LEVEL_MODERATE, choices=ACTIVITY_LEVEL_CHOICES)
    goal = models.CharField(max_length=10, choices=GOAL_CHOICES, default=GOAL_MAINTAIN)


