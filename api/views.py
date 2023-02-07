from django.shortcuts import render
from .serializers import RestaurantSerializer, ItemSerializer
from rest_framework.viewsets import ModelViewSet
from .models import Restaurant, Item


class RestaurantViewSet(ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

# class ItemViewSet(ModelViewSet):
#     serializer_class = ItemSerializer

#     def get_queryset(self):
#         name = self.request.query_params.get('restaurant')
#         if name is None:
#             queryset=Item.objects.all()
#         else:
#             queryset = Item.objects.filter(restaurant__restaurant_name__contains=name).select_related("restaurant")
            
#         return queryset

class ItemViewSet(ModelViewSet):
    serializer_class = ItemSerializer

    def get_queryset(self):
        name = self.request.query_params.get('restaurant')
        restaurantNames = ["burger king", "7-eleven"]
        if name is None:
            queryset=Item.objects.all()
        else:
            queryset = Item.objects.filter(restaurant__restaurant_name__in=restaurantNames).select_related("restaurant")
            
        return queryset