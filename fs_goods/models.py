from django.db import models


# 商品类型分类模型
class TypeInfo(models.Model):
    title = models.CharField(max_length=20, verbose_name='分类标题')
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '商品类型'
        verbose_name_plural = '商品类型'


# 具体某一个商品的相关信息模型类
class GoodsInfo(models.Model):
    # 商品名称
    g_title = models.CharField(max_length=20, verbose_name='商品名称')
    # 商品图片
    g_pic = models.ImageField(upload_to='fs_goods/%Y/%m', verbose_name='商品图片')
    # 商品价格 max_digits=5数字的总位数
    # decimal_places=2小数位数，FloatField()不好控制小数位数。
    g_price = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='商品价格')
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')
    # 商品计价单位
    g_unit = models.CharField(max_length=20, default='500g', verbose_name='商品计价')
    # 商品有按照人气排序，所以设置一个点击量
    g_click = models.IntegerField(verbose_name='商品浏览量')
    # 以上是商品列表页的相关数据提取，接下来是商品详情页中数据的分析提取。
    # 商品简介
    g_abstract = models.CharField(max_length=200, verbose_name='商品简介')
    # 商品库存
    g_stock = models.IntegerField(verbose_name='商品库存')
    # 商品详情介绍

    g_content = models.TextField(verbose_name='商品详情')
    # 该商品对应的是哪一个商品分类，需要设置外键关联。
    g_type = models.ForeignKey(TypeInfo, verbose_name='所属分类', on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.g_title

    class Meta:
        verbose_name = '商品信息'
        verbose_name_plural = '商品信息'

