from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse
from fs_cart.models import CartModel
from fs_goods.models import GoodsInfo
from fs_user.models import UserInfo
from .models import OrderInfo, OrderDetailInfo


# def order(request):
#     """
#     购物车点击结算，进入订单确认页面，订单确认无误，再提交订单，生成订单信息；
#     :param request:
#     :return:
#     """
#     user = UserInfo.objects.get(id=int(request.session.get('user_id')))
#     carts_id = request.GET.get('carts_id').split(';') # ['1', '22', '12']
#     carts = []
#     for cart_id in carts_id:
#         if cart_id:
#             cart = CartModel.objects.get(id=int(cart_id))
#             carts.append(cart)
#     total_price = request.GET.get('total_price')
#     total_count = request.GET.get('total_count')
#     context = {
#         'title': '生鲜-个人订单',
#         'tab_name': '个人订单',
#         'has_sub': 1,
#         'carts': carts,
#         'total_price': total_price,
#         'total_count': total_count,
#         'user': user
#     }
#     return render(request, 'fs_order/place_order.html', context)
def order(request):
    user = UserInfo.objects.get(id=int(request.session.get('user_id')))
    carts_id = request.GET.getlist('cart_id')
    carts = []
    for cart_id in carts_id:
        if cart_id:
            cart = CartModel.objects.get(id=int(cart_id))
            carts.append(cart)
    context = {
        'title': '生鲜-个人订单',
        'tab_name': '个人订单',
        'has_sub': 1,
        'carts': carts,
        'user': user
    }
    return render(request, 'fs_order/place_order.html', context)


def add(request):
    """
    添加订单
    :param request:
    :return:
    """
    cartids = request.POST.get('cartids').split(';')
    address = request.POST.get('address')
    total_price = request.POST.get('total_price')

    # 创建订单对象：保存订单的基本信息，时间、总金额、状态
    order = OrderInfo()
    order.user_id = request.session.get('user_id')
    order.order_date = datetime.now()
    order.order_address = address
    order.order_total_price = total_price
    order.save()

    # 创建订单的详细信息: 一个OrderDetailInfo()对象，对应着一个商品
    for cartid in cartids:
        if cartid:
            cart = CartModel.objects.get(id=int(cartid))
            order_detail = OrderDetailInfo()
            order_detail.good = cart.good
            order_detail.order = order
            order_detail.order_detail_price = cart.good.g_price
            order_detail.order_detail_count = cart.count
            order_detail.save()
            # 删除购物车
            cart.delete()

    return HttpResponse('ok')



