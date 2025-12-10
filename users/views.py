from django.contrib.auth.models import User
from django.shortcuts import render, HttpResponse
from django.db.models import Q

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from .forms import LoginForm, RegisterForm

# Create your views here.


# def login_view(request):
#
#     if request.method != 'POST':
#         form = LoginForm()
#     else:
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 return HttpResponse('登陆成功')
#             else:
#                 return HttpResponse("账号或者密码错误！")
#     return render(request, 'users/login.html', {'form': form})
#
#
# def register_view(request):
#
#     if request.method != 'POST':
#         form = RegisterForm()
#     else:
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             new_user = form.save(commit=False)
#             new_user.set_password(form.cleaned_data.get('password'))
#             # 让username等于邮箱即可
#             new_user.username = form.cleaned_data.get('email')
#             new_user.save()
#             return HttpResponse('注册成功')
#
#     context = {'form': form}
#     return render(request, 'users/register.html', context)
#
#
# class MyBackend(ModelBackend):
#     def authenticate(self, request, username=None, password=None):
#         try:
#             user = User.objects.get(Q(username=username)|Q(email=username))
#             if user.check_password(password):   # 加密明文密码
#                 return user
#         except Exception as e:
#             return None



@api_view(['POST'])
def login_api(request):
    """
    登录 API（使用 LoginForm 验证）
    请求体: { "username": "xxx", "password": "yyy" }
    """
    form = LoginForm(data=request.data)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({
                'message': 'Login successful',
                'user_id': user.id,
                'username': user.username
            })
        else:
            return Response({'error': 'Invalid username or password.'}, status=401)
    else:
        return Response({'errors': form.errors}, status=400)


@api_view(['POST'])
def register_api(request):
    """
    注册 API（使用 RegisterForm）
    请求体: {
        "email": "user@example.com",
        "password": "123456",
        "password1": "123456"
    }
    """

    form = RegisterForm(data=request.data)

    if form.is_valid():
        # 创建用户（关键：将 email 作为 username）
        user = form.save(commit=False)
        user.username = form.cleaned_data['email']
        user.set_password(form.cleaned_data['password'])  # 确保密码加密
        user.save()
        return Response({
            'message': 'Registration successful.',
            'user_id': user.id,
            'username': user.username
        }, status=201)
    else:
        return Response({'errors': form.errors}, status=400)
