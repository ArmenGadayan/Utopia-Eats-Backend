from rest_framework import serializers
from .models import Restaurant, Item

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id', 'restaurant_name']

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'item_name', 'food_category', 'calories', 
                  'total_fat', 'saturated_fat', 'trans_fat', 'cholesterol',
                  'sodium', 'carbohydrates', 'protein', 'sugar', 
                  'dietary_fiber']