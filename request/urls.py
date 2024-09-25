from django.urls import path, re_path
from . import views
from .views import board_list, board_create, board_delete

urlpatterns = [
    re_path(r'^(?P<lang>kor|eng)/$', views.board_list, name='board_list'),
    re_path(r'^(?P<lang>kor|eng)/create/$', views.board_create, name='board_create'),
    re_path(r'^(?P<lang>kor|eng)/delete/<int:request_id>/$', board_delete, name='board_delete'),

]
