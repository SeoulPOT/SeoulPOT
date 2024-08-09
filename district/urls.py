from django.urls import path
from . import views

urlpatterns = [
    path('', views.district, name='district'),
]