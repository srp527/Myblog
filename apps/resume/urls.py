# -*- coding:utf-8 -*- 
__author__ = 'SRP'
__date__ = '2018/5/29 11:42'

from django.urls import path

from .views import MyResumeView


app_name = 'resume'
urlpatterns = [
    path('my_resume', MyResumeView.as_view(),name='my_resume'),

]

