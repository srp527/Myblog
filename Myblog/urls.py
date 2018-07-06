"""Myblog URL Configuration

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
from django.views.static import serve
from django.urls import path,include,re_path
import xadmin
# from rest_framework.authtoken.views import obtain_auth_token

from users.views import IndexView
from Myblog.settings import MEDIA_ROOT ,STATIC_ROOT
# from api.urls import router

urlpatterns = [
    path('api/',include('api.urls',namespace='apii')),
    path('api-auth/',include('rest_framework.urls',namespace='rest_framework')),
    path('cmdb/',include('cmdb.urls',namespace='cmdb')),

    path('xadmin/', xadmin.site.urls),
    # 富文本相关
    path('ueditor/', include('DjangoUeditor.urls')),

    path('', IndexView.as_view(),name='index'),

    path('user/', include('users.urls',namespace='user')),
    path('blog/', include('blogarticle.urls',namespace='blog')),
    path('resume/', include('resume.urls',namespace='resume')),

    re_path('media/(?P<path>.*)',serve,{'document_root': MEDIA_ROOT}),

    # 配置静态文件的访问处理函数
    re_path('static/(?P<path>.*)',serve,{'document_root':STATIC_ROOT}),

]

