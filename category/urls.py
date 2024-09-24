from django.urls import path
from .views import category_choice, district_view, category_district

urlpatterns = [
    # 카테고리 선택 페이지
    path('<str:lang>/', category_choice, name='category_choice'),

    path('<str:lang>/<str:place_tag_cd>/', district_view, name='district_view'),

    # 구 및 카테고리에 따른 장소 조회 (district_id와 place_category_cd 전달)

    path('<str:lang>/<str:place_tag_cd>/<int:district_id>/<str:place_category_cd>/', category_district, name='category_district'),
]


