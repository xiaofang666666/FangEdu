from django.shortcuts import render, redirect, reverse, HttpResponse
from .forms import UserRegisterForm, UserLoginForm
from .models import UserProfile, EmailVerifyCode
from django.db.models import Q
from django.contrib.auth import authenticate,logout,login
from tools.send_mail_tool import send_email_code


# Create your views here.
def index(request):
    return render(request, 'index.html')


def user_register(request):
    if request.method == 'GET':
        #这里实例化forms类不是为了验证，而是为了使用验证码
        user_register_form = UserRegisterForm()
        return render(request, 'register.html',{
            'user_register_form': user_register_form
        })
    else:
        user_register_form = UserRegisterForm(request.POST)
        if user_register_form.is_valid():
            email = user_register_form.cleaned_data['email']
            password = user_register_form.cleaned_data['password']

            user_list = UserProfile.objects.filter(Q(username=email) | Q(email=email))
            if user_list:
                return render(request, 'register.html', {
                    'msg': '用户已存在'
                })
            else:
                a = UserProfile()
                a.username = email
                a.set_password(password)
                a.email = email
                a.save()
                send_email_code(email, 1)
                return HttpResponse('请尽快前往您的邮箱激活，否则无法登陆')
                #return redirect(reverse('index'))
        else:
            return render(request, 'register.html', {
                'user_register_form': user_register_form
            })


def user_login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        user_login_form = UserLoginForm(request.POST)
        if user_login_form.is_valid():
            email = user_login_form.cleaned_data['email']
            password = user_login_form.cleaned_data['password']

            user = authenticate(username=email, password=password)
            print(1)
            if user:
                print(2)
                login(request, user)
                return redirect(reverse('index'))
                if user.is_start:
                    login(request, user)
                    return redirect(reverse('index'))
                else:
                    return HttpResponse('请去您的邮箱激活，否则无法登录')
            else:
                return render(request, 'login.html',{
                    'msg': '邮箱或者密码有误'
                })
        else:
            return render(request, 'login.html', {
                'user_login_form': user_login_form
            })


def user_logout(request):
    logout(request)
    return redirect(reverse('index'))


def user_active(request, code):
    if code:
        email_ver_list = EmailVerifyCode.objects.filter(code=code)
        if email_ver_list:
            email_ver = email_ver_list[0]
            email = email_ver.email
            user_list = UserProfile.objects.filter(username=email)
            if user_list:
                user = user_list[0]
                user.is_start = True
                user.save()
                return redirect(reverse('users:user_login'))
            else:
                pass
        else:
            pass
    else:
        pass
