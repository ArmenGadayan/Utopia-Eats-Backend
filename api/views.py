from django.shortcuts import render
from .serializers import RestaurantSerializer, ItemSerializer
from rest_framework.viewsets import ModelViewSet
from .models import Restaurant, Item
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from difflib import SequenceMatcher
from django.db.models import Count, F, Window
from config import api_key


class RestaurantViewSet(ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

class ItemViewSet(ModelViewSet):
    serializer_class = ItemSerializer

    def get_queryset(self):
        name = self.request.query_params.get('restaurant')
        if name is None:
            queryset=Item.objects.all()
        else:
            queryset = Item.objects.filter(restaurant__restaurant_name__contains=name).select_related("restaurant")
            
        return queryset


class UserItemViewSet(APIView):

    def get(self, request, *args, **kwargs):
        location = request.query_params.get("location")

        if location is None:
            return Response({"bad response": "no location"}, status=status.HTTP_400_BAD_REQUEST)

        lat, lng = location.split(',')
        #lat, lng = 33.64578460229771, -117.84253108132884

        url =("https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=" + str(lat)  + "%2C" + str(lng) + "&radius=1000" +
        "&type=restaurant&key=""" + api_key)
        resp = requests.get(url).json()

        restaurant_list = list(Restaurant.objects.values_list("id", "restaurant_name"))
        
        matches = []
        for result in resp["results"]:
            for r in restaurant_list:
                if SequenceMatcher(None, result["name"], r[1]).ratio() > 0.8:
                    matches.append((result["name"], r[0]))

        queryset = Item.objects.filter(restaurant__id__in=[m[1] for m in matches]).annotate(itemcount=Window(expression=Count("id"), partition_by=[F("restaurant_id")])).order_by("-itemcount").select_related("restaurant")

        serializer = ItemSerializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    

# class ProfileViewSet(ModelViewSet):
#     queryset = Profile.objects.all()
#     serializer_class = ProfileSerializer
#     permission_classes = [IsAuthenticated]

#     @action(detail=False, methods=['GET', 'PUT'])
#     def me(self, request):
#         (profile, created) = Profile.objects.get_or_create(user_id=request.user.id) 
#         if request.method == 'GET':
#             serializer = ProfileSerializer(profile)
#             return Response(serializer.data)
#         elif request.method == 'PUT':
#             serializer = ProfileSerializer(profile, data = request.data)
#             serializer.is_valid(raise_exception=True)
#             serializer.save()
#             return Response(serializer.data)
