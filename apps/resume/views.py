# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.views import View
# Create your views here.


class MyResumeView(View):
    def get(self,request):
        return render(request,'my_resume.html',{ })