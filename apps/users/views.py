# -*- coding:utf-8 -*-
import json

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.urls import reverse

from .models import Users,EmailVerifyRecord
from blogarticle.models import Article
from operation.models import ArticleComments,UserFav
from .forms import LoginForm,RegisterForm,UploadImageForm,UserInfoForm,ModifyPwdForm

# Create your views here.


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = Users.objects.get(Q(username=username)|
                                     Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class IndexView(View):
    '''首页'''
    ###### 1--分页 ####
    def get(self,request):
        all_articles = Article.objects.all().order_by('-add_time')

        # 对文章进行分页显示
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_articles, 6, request=request)  #  第二个参数表示每页显示的个数
        articles = p.page(page)

        return render(request,'index.html',{
            'articles':articles,
        })

    ####### 2--瀑布流 #####
    # def get(self,request):
    #     return render(request, 'index_Pinterest.html', {})


# class GetArticle(View):
#     ####### 2--瀑布流 #####
#     def get(self,request):
#         nid = request.GET.get('nid','')
#         end = request.GET.get('end','')
#         print(nid,end)
#         articles = Article.objects.filter(id__gt=nid).order_by('-add_time').values('id','title','user','desc','add_time')
#         # print(id(articles))
#         articles_list = list(articles)
#         print('--->',articles_list)
#         ret = {
#             'status':True,
#             'data':articles_list
#         }
#         # print(ret)
#         return JsonResponse(ret)
#         # return HttpResponse(json.dumps(ret),content_type='application/json')

class LoginView(View):
    '''用户登录'''

    def get(self,request):
        return render(request,'signin.html',{ })

    def post(self,request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get('email','')
            pass_word = request.POST.get('passwd','')

            # authenticate() Django向数据库验证用户密码是否正确  login才是登录
            user = authenticate(username=user_name,password=pass_word)
            if user is not None:
                user1 = Users.objects.get(Q(username=user_name) | Q(email=user_name))
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return render(request, 'signin.html', {'msg': '用户名或密码错误'})
                # f={'status': 'fail', 'data': 'email', 'message': 'Email not exist.'}
                # return HttpResponse(json.dumps(f),content_type='application/json',charset='utf-8')
        else:
            return render(request, 'signin.html', {'login_form':login_form })


class LogoutView(View):
    '''注销登录'''

    def get(self,request):
        logout(request)
        return HttpResponseRedirect(reverse('index'))


class RegisterView(View):
    '''用户注册'''

    def get(self,request):
        # register_form = RegisterForm()
        return render(request,'register.html',{})

    def post(self,request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get('name','')
            email = request.POST.get('email','')
            passwd = request.POST.get('password1','')
            user_in_db = Users.objects.filter(Q(email=email)|Q(username=user_name))
            if user_in_db:
                f = {'status': 'fail','msg':'该邮箱已被注册!'}
                return HttpResponse(json.dumps(f),content_type='application/json')
                # return render(request, 'register.html', {'register_form': register_form, 'msg': '该邮箱已被注册'})
            else:
                user = Users()
                user.username = user_name
                user.email = email
                user.password = make_password(passwd)
                user.save()
                f = {'status': 'success', 'msg': '注册成功!'}
                return HttpResponse(json.dumps(f), content_type='application/json')

        else:
            errors = []
            for error in  register_form.errors:
                errors.append(error)
            f = {'status': 'fail', 'msg': errors}
            return HttpResponse(json.dumps(f), content_type='application/json')
            # return render(request, 'register.html', {'register_form': register_form})


class UserListView(View):
    '''用户列表页'''

    def get(self,request):
        #检测用户是否为admin,是:列出所有用户,不是:列出当前用户
        # if request.user.is_superuser == 0:
        #     users = request.user
        #     return render(request,'manage_users.html',{'users':users})

        all_users = Users.objects.all().order_by('add_time')

        # 分页显示
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_users, 10, request=request)  #  第二个参数表示每页显示的个数
        users = p.page(page)

        return render(request,'manage_users.html',{'users':users})


class AddDelFavView(View):
    '''用户收藏或取消收藏'''

    def post(self,request):
        # 判断用户是否登录
        if not request.user.is_authenticated:
            f = {'status': 'fail', 'msg': '用户未登录'}
            return HttpResponse(json.dumps(f), content_type='application/json')

        fav_id = request.POST.get('fav_id',0)
        fav_type = request.POST.get('fav_type',0)
        exist_records = UserFav.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
        if exist_records:
            # 如果记录已经存在，则表示用户取消收藏
            exist_records.delete()

            if int(fav_type) == 1:
                f = {'status': 'success', 'msg': '收藏文章'}
                return HttpResponse(json.dumps(f), content_type='application/json')
            if int(fav_type) == 2:
                f = {'status': 'success', 'msg': '关注作者'}
                return HttpResponse(json.dumps(f), content_type='application/json')

        else:
            user_fav = UserFav()
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()
                if int(fav_type) == 1:
                    f = {'status': 'success', 'msg': '已收藏文章'}
                    return HttpResponse(json.dumps(f), content_type='application/json')
                if int(fav_type) == 2:
                    f = {'status': 'success', 'msg': '已关注作者'}
                    return HttpResponse(json.dumps(f), content_type='application/json')
            else:
                f = {'status': 'fail', 'msg': '收藏失败'}
                return HttpResponse(json.dumps(f), content_type='application/json')


class UserFavView(View):
    '''用户收藏文章列表页'''

    def get(self,request):
        # 判断用户是否登录
        if not request.user.is_authenticated:
            f = {'status': 'fail', 'msg': '用户未登录'}
            return HttpResponse(json.dumps(f), content_type='application/json')

        article_list = []
        fav_articles = UserFav.objects.filter(user=request.user,fav_type=1)
        for fav_article in fav_articles:
            article_id = fav_article.fav_id
            article = Article.objects.get(id=article_id)
            article_list.append(article)

        # 分页显示
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(article_list, 10, request=request)  # 第二个参数表示每页显示的个数
        all_fav_articles = p.page(page)

        return render(request,'manage_user_fav.html',{
            'all_fav_articles':all_fav_articles,
        })


class UserInfoView(View):
    '''用户详细信息保存'''

    def post(self,request):
        user_info_form = UserInfoForm(request.POST,instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            f = {'status': 'success'}
            return HttpResponse(json.dumps(f),content_type='application/json')
        else:
            f = {'status': 'fail'}
            return HttpResponse(json.dumps(f), content_type='application/json')


class UserImageView(View):
    '''用户头像上传'''

    def post(self,request):
        #instance传的是ModelForm指定的Model，也就是让image_from用上ModelForm的功能
        image_form = UploadImageForm(request.POST,request.FILES,instance=request.user)
        if image_form.is_valid():
            image_form.save()   #直接用Model的save（）保存
            f = {'status':'success'}
            return HttpResponse(json.dumps(f),content_type='application/json')
        else:
            f = {'status': 'fail'}
            return HttpResponse(json.dumps(f), content_type='application/json')


class UserModifyPwdView(View):
    '''修改密码'''
    def post(self,request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1','')
            pwd2 = request.POST.get('password2','')
            if pwd1 != pwd2:
                f = {'status': 'fail', 'msg': '密码不一致!请重新输入'}
                return HttpResponse(json.dumps(f), content_type='application/json')
            user = request.user
            user.password = make_password(pwd2)
            user.save()
            f = {'status': 'success', 'msg': '密码修改成功'}
            return HttpResponse(json.dumps(f), content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')


class UserModifyEmailView(View):
    '''修改绑定邮箱'''
    def post(self,request):
        email = request.POST.get('email','')
        user = Users.objects.filter(email=email)
        if user:
            f = {'email': '邮箱已被注册'}
            return HttpResponse(json.dumps(f), content_type='application/json')
        user1 = Users.objects.get(username=request.user)
        user1.email = email
        user1.save()
        f = {'status': 'success'}
        return HttpResponse(json.dumps(f), content_type='application/json')



