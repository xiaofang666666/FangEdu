"""FangEdu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from .views import user_register, user_login, user_logout, user_active, user_forget, user_reset

urlpatterns = [
    url(r'^user_register/$',user_register, name='user_register'),
    url(r'^user_login/$', user_login, name='user_login'),
    url(r'^user_logout/$', user_logout, name='user_logout'),
    url(r'^user_active/(\w+)/$', user_active, name='user_active'),
    url(r'^user_forget/$', user_forget, name='user_forget'),
    url(r'^user_reset/(\w+)/$', user_reset, name='user_reset')
]
