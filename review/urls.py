# app_name/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.content_reviews, name="reviews"),  # 기본 리뷰 페이지
    path("more/", views.reviews_more, name="reviews_more"),  # 더보기 페이지
]
