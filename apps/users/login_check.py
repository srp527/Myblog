# -*- coding:utf-8 -*- 
__author__ = 'SRP'


from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

'''
在用户点击页面时，先判断用户是否已经登录，没有登录直接跳转到登录界面 

'''


class LoginRequiredMixin(object):

    @method_decorator(login_required(login_url='/user/login/'))
    def dispatch(self,request,*args,**kwargs):
        return super(LoginRequiredMixin,self).dispatch(request,*args,**kwargs)