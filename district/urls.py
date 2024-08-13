from django.urls import path
from . import views

urlpatterns = [
    path('<str:lang>', views.district, name='district'),
]