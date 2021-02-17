from django.shortcuts import render
from .models import OrgInfo, TeacherInfo, CityInfo
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from operations.models import UserLove

# Create your views here.
def org_list(request):
    all_orgs = OrgInfo.objects.all()
    all_citys = CityInfo.objects.all()
    sort_orgs = all_orgs.order_by('-love_num')[:3]

    #按照机构类别进行过滤筛选
    cate = request.GET.get('cate', '')
    if cate:
        all_orgs = all_orgs.filter(category=cate)
    #按照所在地区进行过滤筛选
    cityid = request.GET.get('cityid', '')
    if cityid:
        all_orgs = all_orgs.filter(cityinfo_id=int(cityid))

    #排序
    sort = request.GET.get('sort', '')
    if sort:
        all_orgs = all_orgs.order_by('-'+sort)


    #分页功能
    pagenum = request.GET.get('pagenum', '')
    pa = Paginator(all_orgs, 3)
    try:
        pages = pa.page(pagenum)
    except PageNotAnInteger:
        pages = pa.page(1)
    except EmptyPage:
        pages = pa.page(pa.num_pages)

    return render(request, 'orgs/org-list.html', {
        'all_orgs': all_orgs,
        'pages': pages,
        'all_citys': all_citys,
        'sort_orgs': sort_orgs,
        'cate': cate,
        'cityid': cityid,
        'sort': sort,
    })


def org_detail(request, org_id):
    if org_id:
        org = OrgInfo.objects.filter(id=int(org_id))[0]

        org.click_num += 1
        org.save()

        # 在返回页面数据时，需要返回收藏这个机构的状态，根据状态让模板页面显示收藏还是取消收藏
        lovestatus = False
        if request.user.is_authenticated:
            love = UserLove.objects.filter(love_man=request.user, love_id=int(org_id), love_type=1, love_status=True)
            if love:
                lovestatus = True

        return render(request, 'orgs/org-detail-homepage.html', {
            'org': org,
            'detail_type': 'home',
            'lovestatus': lovestatus
        })


def org_detail_course(request,org_id):
    if org_id:
        org = OrgInfo.objects.filter(id = int(org_id))[0]
        all_course = org.courseinfo_set.all()

        # 在返回页面数据时，需要返回收藏这个机构的状态，根据状态让模板页面显示收藏还是取消收藏
        lovestatus = False
        if request.user.is_authenticated:
            love = UserLove.objects.filter(love_man=request.user, love_id=int(org_id), love_type=1, love_status=True)
            if love:
                lovestatus = True

        # 分页功能
        pagenum = request.GET.get('pagenum', '')
        pa = Paginator(all_course, 2)
        try:
            pages = pa.page(pagenum)
        except PageNotAnInteger:
            pages = pa.page(1)
        except EmptyPage:
            pages = pa.page(pa.num_pages)
        return render(request, 'orgs/org-detail-course.html', {
            'org': org,
            'pages': pages,
            'detail_type': 'course',
            'lovestatus': lovestatus
        })


def org_detail_desc(request, org_id):
    if org_id:
        org = OrgInfo.objects.filter(id=int(org_id))[0]

        # 在返回页面数据时，需要返回收藏这个机构的状态，根据状态让模板页面显示收藏还是取消收藏
        lovestatus = False
        if request.user.is_authenticated:
            love = UserLove.objects.filter(love_man=request.user, love_id=int(org_id), love_type=1, love_status=True)
            if love:
                lovestatus = True

        return render(request, 'orgs/org-detail-desc.html', {
            'org': org,
            'detail_type': 'desc',
            'lovestatus': lovestatus
        })


def org_detail_teacher(request,org_id):
    if org_id:
        org = OrgInfo.objects.filter(id = int(org_id))[0]

        # 在返回页面数据时，需要返回收藏这个机构的状态，根据状态让模板页面显示收藏还是取消收藏
        lovestatus = False
        if request.user.is_authenticated:
            love = UserLove.objects.filter(love_man=request.user, love_id=int(org_id), love_type=1, love_status=True)
            if love:
                lovestatus = True

        return render(request, 'orgs/org-detail-teachers.html', {
            'org': org,
            'detail_type': 'teacher',
            'lovestatus': lovestatus
        })


def teacher_list(request):
    all_teachers = TeacherInfo.objects.all()
    sort_teachers = all_teachers.order_by('-love_num')[:2]

    sort = request.GET.get('sort','')
    if sort:
        all_teachers = all_teachers.order_by('-'+sort)

    # 分页功能
    pagenum = request.GET.get('pagenum', '')
    pa = Paginator(all_teachers, 2)
    try:
        pages = pa.page(pagenum)
    except PageNotAnInteger:
        pages = pa.page(1)
    except EmptyPage:
        pages = pa.page(pa.num_pages)

    return render(request, 'orgs/teachers-list.html', {
        'all_teachers': all_teachers,
        'sort_teachers': sort_teachers,
        'pages': pages,
        'sort': sort,
    })


def teacher_detail(request, teacher_id):
    if teacher_id:
        all_teachers = TeacherInfo.objects.all()
        teacher = TeacherInfo.objects.filter(id=int(teacher_id))[0]
        sort_teachers = all_teachers.order_by('-love_num')[:2]

        teacher.click_num += 1
        teacher.save()

        # lovecourse和loveorg用来存储用户收藏这个东西的状态，在模板当中根据这个状态来确定页面加载时显示的时收藏还是取消收藏
        loveteacher = False
        loveorg = False
        if request.user.is_authenticated:
            love = UserLove.objects.filter(love_id=int(teacher_id), love_type=3, love_status=True, love_man=request.user)
            if love:
                loveteacher = True
            love = UserLove.objects.filter(love_id=teacher.work_company.id, love_type=1, love_status=True,love_man=request.user)
            if love:
                loveorg = True

        return render(request, 'orgs/teacher-detail.html', {
            'teacher': teacher,
            'sort_teachers': sort_teachers,
            'loveteacher': loveteacher,
            'loveorg': loveorg
        })