from .views import category, get_spots_by_category
from django.urls import path

# 받아올 구 : gu
urlpatterns = [
    path('', category, name = "de-food-place"),
    path('get_spots/', get_spots_by_category, name="get_spot_by_category")
]