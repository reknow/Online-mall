from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, InvalidPage, EmptyPage
from .models import *
from fs_cart.models import CartModel


def index(request):
    """
    商品首页数据：所有的商品分类、每个分类包含2个点击量高的商品是推荐商品、每个分类还需要展示4个商品信息。
    :param request:
    :return:
    """
    # 查询购物车商品数量
    carts = CartModel.objects.filter(user_id=request.session.get('user_id'))
    total_count = 0
    if carts:
        for cart in carts:
            total_count += cart.count

    categorys = TypeInfo.objects.all()
    goods = []
    for category in categorys:
        # 根据分类查询对应的所有商品信息
        hot_goods = category.goodsinfo_set.all().order_by('-g_click')[:2]
        show_goods = category.goodsinfo_set.all().order_by('g_price')[:4]
        dic = {'hot_goods': hot_goods, 'show_goods': show_goods, 'category': category.title, 'category_id': category.id}
        goods.append(dic)

    context = {
        'categorys': categorys,
        'goods': goods,
        'has_cart': 1,
        'total_count': total_count
    }
    return render(request, 'fs_goods/index.html', context)


def goods_list(request):
    """
    商品的列表页
    1. 当前商品分类的ID；
    2. 排序方式：默认、价格、人气(浏览量)
    :param request:
    :return:
    """
    # 查询购物车商品数量
    carts = CartModel.objects.filter(user_id=request.session.get('user_id'))
    total_count = 0
    if carts:
        for cart in carts:
            total_count += cart.count
    # 新品推荐：将最新加入数据库的商品取出两个
    news_goods = GoodsInfo.objects.all().order_by('-id')[:2]
    # 根据排序方式，获取当前分类的所有商品，并进行分页
    category_id = int(request.GET.get('category', ''))
    sort_type = request.GET.get('sort_type', '')
    page_number = request.GET.get('page', 1)
    if sort_type == 'default':
        all_goods = GoodsInfo.objects.filter(g_type=category_id).order_by('-id')
    elif sort_type == 'price':
        all_goods = GoodsInfo.objects.filter(g_type=category_id).order_by('-g_price')
    else:
        all_goods = GoodsInfo.objects.filter(g_type=category_id).order_by('-g_click')
    paginator = Paginator(all_goods, 4)
    try:
        page = paginator.page(int(page_number))
    except (EmptyPage, InvalidPage, PageNotAnInteger):
        page = paginator.page(1)
    context = {
        'title': '生鲜-新鲜水果',
        'page': page,
        'all_goods': all_goods,
        'new_goods': news_goods,
        'has_tab': 0,
        'has_cart': 1,
        'is_detail_page': 0,
        'category_id': category_id,
        'sort_type': sort_type,
        'total_count': total_count
    }
    return render(request, 'fs_goods/list.html', context)


def goods_detail(request, goods_id):
    """
    商品详情页
    :param request:
    :param goods_id:
    :return:
    """
    # 查询购物车商品数量
    carts = CartModel.objects.filter(user_id=request.session.get('user_id'))
    total_count = 0
    if carts:
        for cart in carts:
            total_count += cart.count

    goods = GoodsInfo.objects.get(id=goods_id)
    # 将这个商品的浏览次数进行增加
    goods.g_click += 1
    goods.save()

    # 获取新品推荐商品
    news_goods = GoodsInfo.objects.all().order_by('-id')[:2]
    context = {
        'title': '生鲜-{}'.format(goods.g_title),
        'is_detail_page': 1,
        'has_cart': 1,
        'goods': goods,
        'new_goods': news_goods,
        'total_count': total_count
    }
    response = render(request, 'fs_goods/detail.html', context)
    # 默认先从本地COOKIES中读取浏览记录，如果有记录则直接获取，如果没有记录，就把当前这个商品作为浏览记录保存到COOKIES中
    cookies = request.COOKIES.get('goods_cookie', '')
    if cookies == '':
        # 说明是第一次浏览商品详情，本地还没有生成商品的COOKIE信息，那么直接将这个商品的id存到COOKIE。
        cookies = str(goods_id) + ';' # '1;'
    else:
        # 说明不是第一次浏览商品详情，本地已经存在商品的COOKIE信息了；
        # 从'1;2;3;'COOKIE字符串中，取出每一个商品的ID
        goods_id_list = cookies.split(';') # ['1', '2', '3']
        # 判断当前浏览的这个商品的ID是否存在于这个goods_id列表中，存在说明商品之前浏览过，不存在说明之前没有浏览过；
        """
        第一种方案：只考虑Cookie是否存在，不考虑顺序问题；
        if str(goods_id) in goods_id_list:
            return response
        else:
            goods_id_list.insert(0, str(goods_id))
            cookies = ';'.join(goods_id_list)
            response.set_cookie('goods_cookie', cookies)
            return response
        """
        # 第二种方案：考虑Cookie是否存在，同时考虑顺序问题，将最近点击的商品记录展示在最前面；
        if str(goods_id) in goods_id_list:
            # 说明当前这个商品记录已经存在了，将这个记录从COOKIE中删除。
            goods_id_list.remove(str(goods_id))
        goods_id_list.insert(0, str(goods_id))

        if len(goods_id_list) >= 6:
            goods_id_list = goods_id_list[:5]

        cookies = ';'.join(goods_id_list)

    response.set_cookie('goods_cookie', cookies)
    return response
