from django.db import models
from fs_user.models import UserInfo
from fs_goods.models import GoodsInfo


class CartModel(models.Model):
    """
    购物车商品记录表:
    用户和购物车记录数据：一对多关系，同一个用户可以添加多个商品到记录表中；
    商品和购物车记录数据：一对多关系，不同的用户可以添加相同的产品；
    """
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    good = models.ForeignKey(GoodsInfo, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)
