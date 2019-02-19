from hashlib import sha1
from django.shortcuts import render, redirect, HttpResponseRedirect
from .models import UserInfo
from .islogin import islogin
from fs_goods.models import GoodsInfo
from fs_order.models import OrderInfo


def register(request):
    if request.method == 'GET':
        return render(request, 'fs_user/register.html', {'title': '生鲜-注册'})
    elif request.method == 'POST':
        username = request.POST.get('user_name')
        pwd = request.POST.get('pwd')
        cpwd = request.POST.get('cpwd')
        email = request.POST.get('email')

        # 保存用户之前，对密码进行加密
        s = sha1()
        s.update(pwd.encode('utf8'))
        # 相同字符串加密结果是一样的
        sha1_pwd = s.hexdigest()

        user = UserInfo()
        user.u_name = username
        user.u_password = sha1_pwd
        user.u_email = email
        user.save()
        return redirect('/user/login/')


def login(request):
    if request.method == 'GET':
        return render(request, 'fs_user/login.html', {'title': '生鲜-登录'})
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        jizhu = request.POST.get('jizhu')
        # 查询用户名是否存在
        user = UserInfo.objects.filter(u_name=username)
        if user:
            s = sha1()
            s.update(password.encode('utf8'))
            if s.hexdigest() == user[0].u_password:
                url = request.COOKIES.get('url', '')
                if url == '':
                    response_redirect = HttpResponseRedirect('/user/info/')
                else:
                    response_redirect = HttpResponseRedirect(url)
                # 用户名和密码都正确
                if jizhu != 0:
                    response_redirect.set_cookie('u_name', username)
                else:
                    response_redirect.set_cookie('u_name', '')
                # 将用户名同时存储到session中，来表明用户的登录状态
                request.session['username'] = username
                # 将用户ID存入session，后面操作购物车需要使用这个ID，存起来以后，不需要每次都通过查询数据库来获取这个user_id。
                request.session['user_id'] = user[0].id
                return response_redirect
            else:
                # 用户名正确，密码错误
                context = {
                    'title': '天天生鲜-登录',
                    'username': username,
                    'password': password,
                    'error_pwd': 1,
                    'error_username': 0,
                }
                return render(request, 'fs_user/login.html', context)
        else:
            # 用户名错误
            context = {
                'title': '天天生鲜-登录',
                'username': username,
                'password': password,
                'error_pwd': 0,
                'error_username': 1,
            }
            return render(request, 'fs_user/login.html', context)


@islogin
def info(request):
    user = UserInfo.objects.get(u_name=request.session['username'])

    # 从本地COOKIE读取商品浏览记录
    cookies = request.COOKIES.get('goods_cookie', '')
    goods_list = []
    if cookies != '':
        goods_id_list = cookies.split(';')
        for good_id in goods_id_list:
            if good_id != '':
                good = GoodsInfo.objects.get(id=int(good_id))
                goods_list.append(good)

    # 需要定义两个bool类型的变量
    # has_tab：用于设置是否显示 "| 用户中心" 这个标签
    # has_cart：用于设置是否显示 "我的购物车" 这个标签
    context = {
        'title': '生鲜-个人信息',
        'tab_name': '用户中心',
        'has_tab': 1,
        'has_cart': 0,
        'u_email': user.u_email,
        'u_address': user.u_shou_address,
        'info_active': 1,
        'goods_list': goods_list
    }
    return render(request, 'fs_user/user_center_info.html', context)


@islogin
def site(request):
    user = UserInfo.objects.get(u_name=request.session['username'])
    if request.method == 'POST':
        user.u_shou_address = request.POST['u_shou_address']
        user.u_name = request.POST['u_name']
        user.u_postcode = request.POST['u_postcode']
        user.u_phone = request.POST['u_phone']
        user.save()
    context = {
        'title': '生鲜-收货地址',
        'tab_name': '用户中心',
        'has_tab': 1,
        'has_cart': 0,
        'u_address': user.u_shou_address,
        'site_active': 1
    }
    return render(request, 'fs_user/user_center_site.html', context)

@islogin
def order(request):
    # 从数据库中，查询出所有的订单信息
    orders = OrderInfo.objects.filter(user_id=request.session.get('user_id'))
    context = {
        'has_sub': 1,
        'tab_name': '用户中心',
        'title': '生鲜-全部订单',
        'orders': orders
    }
    return render(request, 'fs_user/user_center_order.html', context)