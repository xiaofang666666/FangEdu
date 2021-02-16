from django.shortcuts import render
from .models import CourseInfo
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator

# Create your views here.
def course_list(request):
    all_courses = CourseInfo.objects.all()
    recommend_courses = all_courses.order_by('-add_time')[:3]

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
        'recommend_courses': recommend_courses
    })