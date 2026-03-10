from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.utils.text import get_valid_filename
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.contrib.auth import get_user_model
from datetime import datetime
from django.middleware.csrf import get_token
import os
import json
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from ..models import Avatar

@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            response = JsonResponse({
                'status': 'success',
                'user_id': user.id,
                'username': user.username,
                'email' : user.email,
            })
            request.session.save()
            # 确保跨域安全设置
            response.set_cookie(
                key='sessionid',
                value=request.session.session_key,
                max_age=86400,
                path='/',
                domain=None,  # 开发环境
                secure=False,
                httponly=True,
                samesite='None'
            )
            return response
        return JsonResponse({'status': 'error'}, status=401)
    return JsonResponse({'status': 'method_not_allowed'}, status=405)

# 注册功能
@csrf_exempt
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        User = get_user_model()
        
        if(username == "" or email == "" or password ==""):
            return JsonResponse({'status': 'fail', 'message': '注册信息不全'})

        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            #messages.error(request, '用户名或邮箱已存在')
            return JsonResponse({'status': 'fail', 'message': '用户或邮箱已被使用'})

        if password != confirm_password:
            #messages.error(request, '密码不一致！')
            return JsonResponse({'status': 'fail', 'message': '两次密码不一致'})

        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,  # 自动加密
                is_active=True     # 默认激活
            )
            user.registered_on = datetime.now()
            user.save()
            
            curr_user = User.objects.filter(username = username).first();
            avatar = Avatar.objects.create(user_id = curr_user.id);
            avatar.save();
           # messages.success(request, '注册成功！')
            return JsonResponse({'status': 'success', 'message': '注册成功'})
        except Exception as e:
            #messages.error(request, '注册失败')
            return  JsonResponse({'status': 'fail', 'message': '程序异常'})

    return  JsonResponse({'status': 'fail', 'message': '请求非法!!!'})

# 登出功能
@csrf_exempt
def logout(request):
    """退出登录"""
    request.session.flush()  # 清空Session
    return JsonResponse({'status': 'success'})

#登陆验证
@csrf_exempt
def checkLogin(request):
    #return JsonResponse({"check":'check'})
    User = get_user_model();
    try:
         # 调试输出
        print("="*50)
        print("请求头:", request.headers)
        print("Cookies:", request.COOKIES)
        print("Session:", request.session.items())
        print("用户:", request.user)

        if request.user.is_authenticated:
        # 返回新的CSRF令牌确保后续请求
            avatar = Avatar.objects.filter(user_id = request.user.id).first();
            curr_user = User.objects.filter(id = request.user.id).first();
            response = JsonResponse({
                'status': 'success',
                'username': curr_user.username,
                'user_id': curr_user.id,
                'email' : curr_user.email,
                'avatar': avatar.avatar
            })
            response.set_cookie(
                'csrftoken',
                get_token(request),
                samesite='None',
                secure=False
            )
            return response
    except:
        return JsonResponse({'status': 'fail','message': '服务器内部错误'}, status=505)
    return JsonResponse({'status': 'fail'}, status=401)

# 更新用户信息
@csrf_exempt
@require_http_methods(["POST"])
def update_profile(request):
    try:
        username = request.POST.get('username')
        email = request.POST.get('email')
        user_id = request.POST.get('user_id')
        avatarUrl = request.POST.get('avatar')
    
        User = get_user_model();
        user = User.objects.filter(id=user_id).first();
        user.username = username;
        user.email = email;
        user.save();
    
        avatar = Avatar.objects.filter(user_id = request.user.id).first();
        avatar.avatar = avatarUrl;
        avatar.save();
    except:
        return JsonResponse({'status': 'fail','message':'程序异常'})
    
    
    return JsonResponse({'status': 'success','message':'修改成功！'})

@ensure_csrf_cookie
def csrf_token_view(request):
    return JsonResponse({'status': 'success'})