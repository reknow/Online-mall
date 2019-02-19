from fs_user.models import UserInfo
from fs_goods.models import GoodsInfo
from django.db import models

# Create your models here.
class OrderInfo(models.Model):
    """
    订单的基本信息
    """
    user = models.ForeignKey(UserInfo, on_delete=models.DO_NOTHING)
    order_date = models.DateTimeField(auto_now=True)
    order_status = models.BooleanField(default=False)
    order_total_price = models.CharField(max_length=100)
    order_address = models.CharField(max_length=150)


class OrderDetailInfo(models.Model):
    # 订单商品所属的商品
    good = models.ForeignKey(GoodsInfo, on_delete=models.DO_NOTHING)
    # 订单商品所属的订单编号
    order = models.ForeignKey(OrderInfo, on_delete=models.DO_NOTHING)
    # 订单商品的单价
    order_detail_price = models.CharField(max_length=100)
    # 订单商品的数量
    order_detail_count = models.IntegerField()

