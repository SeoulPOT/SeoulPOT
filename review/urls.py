# app_name/urls.py
from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path(r"^(?P<lang>kor|eng)/$", views.content_reviews, name="reviews"),  # 기본 리뷰 페이지
    re_path(r"^(?P<lang>kor|eng)/more/$", views.reviews_more, name="reviews_more"),  # 더보기 페이지
]
