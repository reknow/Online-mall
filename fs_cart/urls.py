from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('list/', index),
    # 添加购物车，需要知道购买商品和购买数量各是什么。
    path('add/<int:goods_id>/<int:goods_count>/', add),
]