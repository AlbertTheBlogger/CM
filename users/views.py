from django.contrib.auth.models import User
from django.shortcuts import render, HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

# Create your views here.

from .forms import LoginForm, RegisterForm

def login_view(request):

    if request.method != 'POST':
        form = LoginForm()
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponse('登陆成功')
            else:
                return HttpResponse("账号或者密码错误！")
    return render(request, 'users/login.html', {'form': form})


def register_view(request):

    if request.method != 'POST':
        form = RegisterForm()
    else:
        form = RegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data.get('password'))
            # 让username等于邮箱即可
            new_user.username = form.cleaned_data.get('email')
            new_user.save()
            return HttpResponse('注册成功')

    context = {'form': form}
    return render(request, 'users/register.html', context)


class MyBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):   # 加密明文密码
                return user
        except Exception as e:
            return None


