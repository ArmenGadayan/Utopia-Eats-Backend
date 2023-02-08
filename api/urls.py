from django.urls import path
from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()
router.register('restaurants', views.RestaurantViewSet, basename='restaurants')
router.register('items', views.ItemViewSet, basename='items')
router.register('useritems', views.UserItemViewSet, basename='useritems')

#urlpatterns = router.urls

urlpatterns = [
    path('useritems/', views.UserItemViewSet.as_view()),
]
