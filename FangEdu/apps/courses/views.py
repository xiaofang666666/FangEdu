from django.shortcuts import render
from .models import CourseInfo
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from operations.models import UserLove, UserCourse
from django.db.models import Q

# Create your views here.
def course_list(request):
    all_courses = CourseInfo.objects.all()
    recommend_courses = all_courses.order_by('-add_time')[:3]

    # 全局搜索功能的过滤
    keyword = request.GET.get('keyword', '')
    if keyword:
        all_courses = all_courses.filter(Q(name__icontains=keyword) | Q(desc__icontains=keyword) | Q(detail__icontains=keyword))

    sort = request.GET.get('sort', '')
    if sort:
        all_courses = all_courses.order_by('-'+sort)

    # 分页功能
    pagenum = request.GET.get('pagenum', '')
    pa = Paginator(all_courses, 3)
    try:
        pages = pa.page(pagenum)
    except PageNotAnInteger:
        pages = pa.page(1)
    except EmptyPage:
        pages = pa.page(pa.num_pages)

    return render(request, 'courses/course-list.html', {
        'all_courses': all_courses,
        'pages': pages,
        'recommend_courses': recommend_courses,
        'sort': sort,
        'keyword': keyword,
    })


def course_detail(request, course_id):
    if course_id:
        course = CourseInfo.objects.filter(id=int(course_id))[0]
        relate_courses = CourseInfo.objects.filter(catagory=course.catagory).exclude(id=int(course_id))[:2]

        course.click_num += 1
        course.save()

        #lovecourse和loveorg用来存储用户收藏这个东西的状态，在模板当中根据这个状态来确定页面加载时显示的时收藏还是取消收藏
        lovecourse = False
        loveorg = False
        if request.user.is_authenticated:
            love = UserLove.objects.filter(love_id=int(course_id), love_type=2, love_status=True, love_man=request.user)
            if love:
                lovecourse = True
            love = UserLove.objects.filter(love_id=course.orginfo.id, love_type=1, love_status=True, love_man=request.user)
            if love:
                loveorg = True
        return render(request, 'courses/course-detail.html', {
            'course': course,
            'relate_courses': relate_courses,
            'lovecourse':lovecourse,
            'loveorg':loveorg
        })


def course_video(request,course_id):
    if course_id:
        course = CourseInfo.objects.filter(id=int(course_id))[0]

        # 当用户点击开始学习后，，代表这个用户学习了这个课程，我们需要去判断用户学习课
        # 程的表当中有没有学习这门课程的记录，如果没有，需要加上这条记录
        usercourse_list = UserCourse.objects.filter(study_man=request.user, study_course=course)
        if not usercourse_list:
            a = UserCourse()
            a.study_man = request.user
            a.study_course = course
            a.save()
            course.study_num += 1
            course.save()

            # 第一步：从学习课程的表中查找当前这个人学习的所有课程
            usercourse_list = UserCourse.objects.filter(study_man=request.user)
            course_list = [usercourse.study_course for usercourse in usercourse_list]
            # 第二步：根据拿到的所有课程，找到每个课程的机构
            org_list = list(set([course.orginfo for course in course_list]))

            if course.orginfo not in org_list:
                course.orginfo.study_num += 1
                course.orginfo.save()

        # 学过该课的同学还学过什么课程
        # 第一步：我们需要从中间表用户课程表中找到学过该科的所有对象
        usercourse_list = UserCourse.objects.filter(study_course=course)
        # 第二步：根据找到的用户学习课程列表遍历拿到所有学习过这门课程的用户列表
        user_list = [usercourse.study_man for usercourse in usercourse_list]
        # 第三步：再根据找到的用户，从中间学习课程表中，找到所有用户学习其它课程的整个对象,并去除当前课程
        usercourse_list = UserCourse.objects.filter(study_man__in=user_list).exclude(study_course=course)
        # 第四步：从获取到的用户课程列表中拿到我们需要的其它课程
        course_list = [usercourse.study_course for usercourse in usercourse_list]

        return render(request, 'courses/course-video.html', {
            'course': course,
            'course_list': course_list
        })


def course_comment(request, course_id):
    course = CourseInfo.objects.filter(id=int(course_id))[0]
    all_comment = course.usercomment_set.all()[:10]

    # 上过该课的同学还学过什么课程
    # 第一步：我们需要从中间表用户课程表中找到学过该课的所有对象
    usercourse_list = UserCourse.objects.filter(study_course=course)
    # 第二步：根据找到的用户学习课程列表遍历拿到所有学习过这门课程的用户列表
    user_list = [usercourse.study_man for usercourse in usercourse_list]
    # 第三步：再根据找到的用户，从中间学习课程表中，找到所有用户学习其它课程的整个对象,并去除当前课程
    usercourse_list = UserCourse.objects.filter(study_man__in=user_list).exclude(study_course=course)
    # 第四步：从获取到的用户课程列表中拿到我们需要的其它课程
    course_list = [usercourse.study_course for usercourse in usercourse_list]

    return render(request, 'courses/course-comment.html', {
        'course': course,
        'all_comment': all_comment,
        'course_list': course_list,
    })