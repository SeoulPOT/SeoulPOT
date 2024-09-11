from django.urls import path
from .views import category, district

urlpatterns = [
    path('<str:lang>/', category, name='category_view'),
    path('<str:lang>/<str:place_category_cd>/', district, name='district_category'),
]





