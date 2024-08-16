from django.urls import path
from .views import content_reviews

urlpatterns = [
    path('reviews/<int:place_id>/', content_reviews, name='project-content_reviews'),
]

#place_id를 받고 이동
