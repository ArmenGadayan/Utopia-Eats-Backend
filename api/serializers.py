from rest_framework import serializers
from .models import Restaurant, Item 

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id', 'restaurant_name']

class ItemSerializer(serializers.ModelSerializer):
    restaurant_name = serializers.CharField(source='restaurant.restaurant_name')

    class Meta:
        model = Item
        fields = ['id', 'item_name', 'food_category', 'calories', 
                  'total_fat', 'saturated_fat', 'trans_fat', 'cholesterol',
                  'sodium', 'carbohydrates', 'protein', 'sugar', 
                  'dietary_fiber', 'restaurant_id', 'restaurant_name']
        
# class ProfileSerializer(serializers.ModelSerializer):
#     user_id = serializers.IntegerField(read_only=True)

#     class Meta:
#         model = Profile
#         fields = ['id', 'user_id', 'weight', 'height_feet', 'height_inches']