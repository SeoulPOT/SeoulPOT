from django.urls import path
from . import views
from .views import board_list, board_create, board_delete

urlpatterns = [
    path('', views.board_list, name='board_list'),
    path('create/', views.board_create, name='board_create'),
    path('delete/<int:request_id>/', board_delete, name='board_delete'),

]
