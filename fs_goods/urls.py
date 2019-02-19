from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('index/', index),
    path('list/', goods_list),
    path('detail/<int:goods_id>/', goods_detail)
]