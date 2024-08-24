from django.urls import path
from . import views

urlpatterns = [
    path('<int:place_id>/<str:place_category_cd>/<str:place_tag_cd>/', views.content_reviews, name='project-content_reviews'),
]
