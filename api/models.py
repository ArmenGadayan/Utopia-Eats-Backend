from django.db import models


class Restaurant(models.Model):
    restaurant_name = models.CharField(max_length=255)

    def __str__(self):
        return self.restaurant_name
    
class Item(models.Model):
    item_name = models.CharField(max_length=255)
    food_category = models.CharField(max_length=255, null=True, blank=True)
    calories = models.FloatField()
    total_fat = models.FloatField(null=True, blank=True)
    saturated_fat = models.FloatField(null=True, blank=True)
    trans_fat = models.FloatField(null=True, blank=True)
    cholesterol = models.FloatField(null=True, blank=True)
    sodium = models.FloatField(null=True, blank=True)
    carbohydrates = models.FloatField(null=True, blank=True)
    protein = models.FloatField(null=True, blank=True)
    sugar = models.FloatField(null=True, blank=True)
    dietary_fiber = models.FloatField(null=True, blank=True)

    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='item')
