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
from django.db.models import Count, F, Window, Value
from config import api_key
import time


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
        user = self.request.user
        sex = "Male"

        weight = 180*0.453592
        height = (6*12 + 0)*2.54

        if sex == "Male":
            bmr = 10*weight + 6.25*height - 5*21 + 5

        calories = bmr* 1.55

        # if user.goal == "Lose":
        #     calories = calories*0.85
        # elif user.goal == "Gain":
        #     calories += 500

        calories = calories/3
        
        carbs = (calories * 0.4)/4
        # if user.goal == "Lose":
        #     protein = (calories*0.4)/4
        #     fats = (calories*0.2)/9
        # else:
        protein = (calories*0.3)/4
        fats = (calories*0.3)/9

        calories_floor = calories*0.85
        calories_ceiling = calories*1.15
        carbs_floor = carbs*0.8
        carbs_ceiling = carbs*1.2
        protein_floor = protein*0.8
        protein_ceiling = protein*1.2
        fats_floor = fats*0.8
        fats_ceiling = fats*1.2

        location = request.query_params.get("location")

        # if location is None:
        #     return Response({"bad response": "no location"}, status=status.HTTP_400_BAD_REQUEST)

        #lat, lng = location.split(',')

        lat, lng = 33.64578460229771, -117.84253108132884

        url =("https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=" + str(lat)  + "%2C" + str(lng) + "&radius=10000" +
        "&type=restaurant&key=""" + api_key)
        resp = requests.get(url).json()

        restaurant_list = list(Restaurant.objects.values_list("id", "restaurant_name"))
        
        matches = []
        for result in resp["results"]:
            for r in restaurant_list:
                if SequenceMatcher(None, result["name"], r[1]).ratio() > 0.8:
                    matches.append((result["name"], r[0]))


        try:
            token = resp["next_page_token"]
            if token:
                url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?pagetoken=" + token + "&key=" + api_key
                time.sleep(2)
                resp = requests.get(url).json()

                for result in resp["results"]:
                    for r in restaurant_list:
                        if SequenceMatcher(None, result["name"], r[1]).ratio() > 0.8:
                            matches.append((result["name"], r[0]))
        except KeyError:
            pass

        try:
            token = resp["next_page_token"]
            if token:
                url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?pagetoken=" + token + "&key=" + api_key
                time.sleep(2)
                resp = requests.get(url).json()

                for result in resp["results"]:
                    for r in restaurant_list:
                        if SequenceMatcher(None, result["name"], r[1]).ratio() > 0.8:
                            matches.append((result["name"], r[0]))
        except KeyError:
            pass

        # queryset = Item.objects.filter(restaurant__id__in=[m[1] for m in matches]).filter(calories__gte = calories_floor, calories__lte = calories_ceiling, 
        #     carbohydrates__gte = carbs_floor, carbohydrates__lte = carbs_ceiling, protein__gte = protein_floor, protein__lte = protein_ceiling, 
        #     total_fat__gte = fats_floor, total_fat__lte = fats_ceiling).annotate(itemcount=Window(expression=Count("id"), partition_by=[F("restaurant_id")])).order_by("-itemcount").select_related("restaurant")
        
        allMatch = Item.objects.filter(restaurant__id__in=[m[1] for m in matches]).filter(calories__gte = calories_floor, calories__lte = calories_ceiling, 
            carbohydrates__gte = carbs_floor, carbohydrates__lte = carbs_ceiling, protein__gte = protein_floor, protein__lte = protein_ceiling, 
            total_fat__gte = fats_floor, total_fat__lte = fats_ceiling).annotate(score=Value(4)).select_related("restaurant")
        
        carbProteinMatch = Item.objects.filter(restaurant__id__in=[m[1] for m in matches]).filter(calories__gte = calories_floor, calories__lte = calories_ceiling, 
            carbohydrates__gte = carbs_floor, carbohydrates__lte = carbs_ceiling, protein__gte = protein_floor, protein__lte = protein_ceiling).exclude(id__in=allMatch.values_list("id", flat=True)).annotate(score=Value(3)).select_related("restaurant")
        
        carbFatsMatch = Item.objects.filter(restaurant__id__in=[m[1] for m in matches]).filter(calories__gte = calories_floor, calories__lte = calories_ceiling, 
            carbohydrates__gte = carbs_floor, carbohydrates__lte = carbs_ceiling, total_fat__gte = fats_floor, total_fat__lte = fats_ceiling).exclude(id__in=allMatch.values_list("id", flat=True)).annotate(score=Value(3)).select_related("restaurant")
        
        fatsProteinMatch = Item.objects.filter(restaurant__id__in=[m[1] for m in matches]).filter(calories__gte = calories_floor, calories__lte = calories_ceiling, 
            total_fat__gte = fats_floor, total_fat__lte = fats_ceiling, protein__gte = protein_floor, protein__lte = protein_ceiling).exclude(id__in=allMatch.values_list("id", flat=True)).annotate(score=Value(3)).select_related("restaurant")
        
        proteinMatch = Item.objects.filter(restaurant__id__in=[m[1] for m in matches]).filter(calories__gte = calories_floor, calories__lte = calories_ceiling, 
            protein__gte = protein_floor, protein__lte = protein_ceiling).exclude(id__in=carbProteinMatch.values_list("id", flat=True)).exclude(id__in=fatsProteinMatch.values_list("id", flat=True)).exclude(id__in=allMatch.values_list("id", flat=True)).annotate(score=Value(2)).select_related("restaurant")
        
        carbMatch = Item.objects.filter(restaurant__id__in=[m[1] for m in matches]).filter(calories__gte = calories_floor, calories__lte = calories_ceiling, 
            carbohydrates__gte = carbs_floor, carbohydrates__lte = carbs_ceiling).exclude(id__in=carbFatsMatch.values_list("id", flat=True)).exclude(id__in=carbProteinMatch.values_list("id", flat=True)).exclude(id__in=allMatch.values_list("id", flat=True)).annotate(score=Value(2)).select_related("restaurant")
        
        fatsMatch = Item.objects.filter(restaurant__id__in=[m[1] for m in matches]).filter(calories__gte = calories_floor, calories__lte = calories_ceiling, 
            total_fat__gte = fats_floor, total_fat__lte = fats_ceiling).exclude(id__in=carbFatsMatch.values_list("id", flat=True)).exclude(id__in=fatsProteinMatch.values_list("id", flat=True)).exclude(id__in=allMatch.values_list("id", flat=True)).annotate(score=Value(2)).select_related("restaurant")
        
        result = allMatch.union(carbProteinMatch, carbFatsMatch, fatsProteinMatch, proteinMatch, carbMatch, fatsMatch, all=True).order_by("-score")

        serializer = ItemSerializer(result, many=True)

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
