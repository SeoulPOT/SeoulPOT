from django.urls import path
from . import views

urlpatterns = [
    path('', views.content_reviews, name='project-content_reviews'),
]
