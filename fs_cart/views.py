from django.shortcuts import render
from django.http import JsonResponse
from .models import CartModel
from fs_user.models import UserInfo
from fs_goods.models import GoodsInfo
from fs_user.islogin import islogin


@islogin
def index(request):
    """
    购物车列表数据。
    :param request:
    :return:
    """
    user_id = request.session.get('user_id', '')
    carts_record = CartModel.objects.filter(user_id=user_id)
    context = {
        'title': '生鲜-购物车',
        'has_tab': 1,
        'tab_name': '购物车',
        'carts_record': carts_record
    }
    return render(request, 'fs_carts/cart.html', context)


@islogin
def add(request, goods_id, goods_count):
    """
    添加商品到购物车
    :param request:
    :return:
    """
    user_id = request.session.get('user_id', '')
    # 这个商品在添加购物车之前，先判断购物车中是否已经存在这个商品了，如果已经存在只需要让数量进行增加即可，如果购物车中不存在，在生成购物车记录到表中；
    cart = CartModel.objects.filter(user_id=user_id, good_id=goods_id)
    if cart:
        cart[0].count = cart[0].count + goods_count
        cart[0].save()
    else:
        cart = CartModel(user_id=user_id, good_id=goods_id, count=goods_count)
        cart.save()

    # 查询当前用户购物车记录表中所有的商品数量总和
    carts = CartModel.objects.filter(user_id=user_id)
    total_count = 0
    for cart in carts:
        total_count += cart.count
    return JsonResponse({'total_count': total_count})

# 支付宝支付；
# Django的中间件执行过程，自定义中间件；
# Django的数据缓存；
