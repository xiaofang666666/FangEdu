from django.shortcuts import render, redirect, reverse, HttpResponse
from .forms import UserRegisterForm, UserLoginForm, UserForgetForm, UserResetForm
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
        return render(request, 'users/register.html',{
            'user_register_form': user_register_form
        })
    else:
        user_register_form = UserRegisterForm(request.POST)
        if user_register_form.is_valid():
            email = user_register_form.cleaned_data['email']
            password = user_register_form.cleaned_data['password']

            user_list = UserProfile.objects.filter(Q(username=email) | Q(email=email))
            if user_list:
                return render(request, 'users/register.html', {
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
            return render(request, 'users/register.html', {
                'user_register_form': user_register_form
            })


def user_login(request):
    if request.method == 'GET':
        return render(request, 'users/login.html')
    else:
        user_login_form = UserLoginForm(request.POST)
        if user_login_form.is_valid():
            email = user_login_form.cleaned_data['email']
            password = user_login_form.cleaned_data['password']

            user = authenticate(username=email, password=password)
            if user:
                login(request, user)
                return redirect(reverse('index'))
                if user.is_start:
                    login(request, user)
                    return redirect(reverse('index'))
                else:
                    return HttpResponse('请去您的邮箱激活，否则无法登录')
            else:
                return render(request, 'users/login.html', {
                    'msg': '邮箱或者密码有误'
                })
        else:
            return render(request, 'users/login.html', {
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


def user_forget(request):
    if request.method == 'GET':
        user_forget_form = UserForgetForm()
        return render(request, 'users/forgetpwd.html', {
            'user_forget_form': user_forget_form
        })
    else:
        user_forget_form = UserForgetForm(request.POST)
        if user_forget_form.is_valid():
            email = user_forget_form.cleaned_data['email']
            user_list = UserProfile.objects.filter(email=email)
            if user_list:
                send_email_code(email, 2)
                return HttpResponse('请尽快到您的邮箱重置密码')
            else:
                return render(request, 'users/forgetpwd.html',{
                    'msg': '用户不存在'
                })
        else:
            return render(request, 'users/forgetpwd.html', {
                'user_forget_form': user_forget_form
            })


def user_reset(request, code):
    if code:
        if request.method == 'GET':
            return render(request, 'users/password_reset.html', {
                'code': code
            })
        else:
            user_reset_form = UserResetForm(request.POST)
            if user_reset_form.is_valid():
                password = user_reset_form.cleaned_data['password']
                password1 = user_reset_form.cleaned_data['password1']
                if password == password1:
                    email_ver_list = EmailVerifyCode.objects.filter(code=code)
                    if email_ver_list:
                        email_ver = email_ver_list[0]
                        email = email_ver.email
                        user_list = UserProfile.objects.filter(email=email)
                        if user_list:
                            user = user_list[0]
                            user.set_password(password1)
                            user.save()
                            return redirect(reverse('users:user_login'))
                        else:
                            pass
                    else:
                        pass
                else:
                    return render(request, 'users/password_reset.html', {
                        'msg': '两次密码不一致',
                        'code': code
                    })
            else:
                return render(request, 'users/password_reset.html', {
                    'user_reset_form': user_reset_form,
                    'code': code
                })