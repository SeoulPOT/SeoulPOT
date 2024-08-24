from django.urls import path,re_path
from .views import district, get_places_by_districts, get_places_by_category

urlpatterns = [
    path('<str:lang>/', district, name='district'), #html에서 얘로 부르기
    # path('eng/', district, name='district-eng'), 
    path('kor/<int:district_id>', get_places_by_districts, name='dictrict'),
    re_path(r'^(?P<lang>kor|eng)/(?P<district_id>\d+)/(?P<place_category_cd>\w+)/$', get_places_by_category, name='category'),
    # re_path(r'^category/(?P<lang>kor|eng)/(?P<district_id>\d+)/(?P<place_category_cd>\w+)/$', get_places_by_category, name='category'),
]