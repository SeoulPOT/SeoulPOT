from .views import category, get_spots_by_category
from django.urls import path, re_path

# 받아올 구 : gu
urlpatterns = [
    re_path(r'^(?P<lang>kor|eng)/', category, name = "de-food-place"),
    path('get_spots/', get_spots_by_category, name="get_spot_by_category")
]
