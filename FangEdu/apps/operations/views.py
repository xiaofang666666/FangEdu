from django.shortcuts import render
from .forms import UserAskForm
#from .models import UserAsk
from django.http import JsonResponse
from .models import UserLove

# Create your views here.
def user_ask(request):
    user_ask_form = UserAskForm(request.POST)
    if user_ask_form.is_valid():
        user_ask_form.save(commit=True)
        # name = user_ask_form.cleaned_data['name']
        # phone = user_ask_form.cleaned_data['phone']
        # course = user_ask_form.cleaned_data['course']
        #
        # a = UserAsk()
        # a.name = name
        # a.phone = phone
        # a.course = course
        # a.save()
        return JsonResponse({'status': 'ok', 'msg': '咨询成功'})
    else:
        return JsonResponse({'status': 'fail', 'msg': '咨询失败'})


def user_love(request):
    loveid = request.GET.get('loveid', '')
    lovetype = request.GET.get('lovetype', '')
    if loveid and lovetype:
        #如果收藏的id和type同时存在，那么我们首先要去收藏表当中去查找有没有这个收藏记录
        love = UserLove.objects.filter(love_id=int(loveid), love_type=int(lovetype), love_man=request.user)
        if love:
            # 如果已经存在收藏这个东西的记录，那么我们需要判断收藏的状态，如果收藏状态为真，
            # 代表之前收藏过，并且现在的页面上应先显示的是取消收藏，代表着这次点击是为了取消收藏
            if love[0].love_status:
                love[0].love_status = False
                love[0].save()
                return JsonResponse({'status': 'ok', 'msg': '收藏'})
            # 如果收藏状态为假，代表之前收藏过，并且又取消了收藏，并且现在页面上应显示的是收藏，代表着这次点击是为了收藏
            else:
                love[0].love_status = True
                love[0].save()
                return JsonResponse({'status': 'ok', 'msg': '取消收藏'})
        else:
            #如果之前没有收藏过这个东西，那么代表表当中没有这个记录，我们需要创建这个记录对象，然后把这个记录的状态改为true
            a = UserLove()
            a.love_man = request.user
            a.love_id = int(loveid)
            a.love_type = int(lovetype)
            a.love_status = True
            a.save()
            return JsonResponse({'status': 'ok', 'msg': '取消收藏'})
    else:
        return JsonResponse({'status': 'ok', 'msg': '收藏失败'})