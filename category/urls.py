from django.urls import path, re_path
from .views import category_choice, district_view, category_district

# urlpatterns = [
#     # 카테고리 선택 페이지
#     path('<str:lang>/', category_choice, name='category_choice'),

#     path('<str:lang>/<str:place_tag_cd>/', district_view, name='district_view'),

#     # 구 및 카테고리에 따른 장소 조회 (district_id와 place_category_cd 전달)
#     path('<str:lang>/<str:place_tag_cd>/<int:district_id>/<str:place_category_cd>/<place_thema_cd>/', category_district, name='category_district'),
# ]


urlpatterns = [
    # 카테고리 선택 페이지
    re_path(r'^(?P<lang>\w{2,3})/$', category_choice, name='category_choice'),

    # place_tag_cd가 포함된 URL
    re_path(r'^(?P<lang>\w{2,3})/(?P<place_thema_cd>\w+)/$', district_view, name='district_view'),

    # 구 및 카테고리에 따른 장소 조회 (district_id와 place_category_cd 전달)
    re_path(r'^(?P<lang>\w{2,3})/(?P<district_id>\d+)/(?P<place_category_cd>\w+)/(?P<place_thema_cd>\w+)/$', category_district, name='category_district'),
]

