from django.urls import path
from .views import get_sever_time

urlpatterns = [
    path('', get_sever_time, name='main')
]