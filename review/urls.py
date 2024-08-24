from django.urls import path
from . import views

urlpatterns = [
    path('', views.content_reviews, name='review'),
]


#place_id를 받고 이동
