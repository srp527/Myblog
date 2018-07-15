# -*- coding:utf-8 -*-
import json
import base64

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse

from .models import Article,Category
from operation.models import ArticleComments,ArticleReplyComments,UserFav
from users.models import Users
from users.login_check import LoginRequiredMixin
# Create your views here.


class ArticleView(View):
    '''文章内容页'''
    def get(self,requset,article_id):
        article_detail = Article.objects.get(id=article_id)
        # article_child_comments = ArticleReplyComments.objects.all().order_by('add_time')
        all_users = Users.objects.all()

        article_detail.click_nums += 1
        article_detail.save()

        # 判断用户是否已收藏改文章/作者
        has_fav_article = False
        has_fav_user = False
        if requset.user.is_authenticated:
            article_fav = UserFav.objects.filter(user=requset.user,fav_id=article_id,fav_type=1 )
            user_fav = UserFav.objects.filter(user=requset.user,fav_id=article_detail.user.id,fav_type=2 )
            if article_fav:
                has_fav_article = True
            if user_fav:
                has_fav_user = True

        return render(requset,'article_detail.html',{
                'article_detail': article_detail ,
                # 'article_comments': article_comments,
                # 'article_child_comments':article_child_comments,
                'all_users':all_users,
                'has_fav_article':has_fav_article,
                'has_fav_user':has_fav_user,

            })


class ArticleListView(View):
    '''文章列表页'''

    def get(self,request):
        all_articles = Article.objects.all().order_by('-add_time')
        if request.user.is_authenticated:
            art_favs = UserFav.objects.filter(user=request.user)
            # 对文章列表进行分页显示
            try:
                page = request.GET.get('page', 1)
            except PageNotAnInteger:
                page = 1
            p = Paginator(all_articles, 10, request=request)  # 3 第二个参数表示每页显示的个数
            articles = p.page(page)

            return render(request, 'manage_article_list.html', {
                'articles': articles,
                'art_favs': art_favs,
            })

        # 对文章列表进行分页显示
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_articles, 10, request=request)  # 3 第二个参数表示每页显示的个数
        articles = p.page(page)

        return render(request,'manage_article_list.html',{
            'articles':articles,
        })


class ArticleAddView(LoginRequiredMixin,View):
    '''添加新文章'''

    def get(self,request):
        all_categorys = Category.objects.all()

        return render(request,'article_add.html',{
            'all_categorys':all_categorys,
        })

    def post(self,request):
        # 先判断用户是否登录
        # if not request.user.is_authenticated:
        #     f = {'status': 'fail', 'msg': '用户未登录'}
        #     return HttpResponse(json.dumps(f), content_type='application/json')
        art_title = request.POST.get('title','')
        art_desc = request.POST.get('desc','')
        art_content = request.POST.get('content','')
        art_category = request.POST.get('category','')
        art_user = request.user
        # print('art_category',art_category)
        art_category = Category.objects.get(id=art_category)
        article = Article(title=art_title,desc=art_desc,content=art_content,user=art_user,category=art_category)
        article.save()
        # art_id = article.id
        # f1 = {'status': 'success','art_id':art_id}  #传个 art_id过去 保存后可以直接跳转到文章详情页
        f1 = {'status': 'success', 'msg': '发表成功'}
        return HttpResponse(json.dumps(f1), content_type='application/json')


class AddCategoryView(View):
    '''添加文章类型'''
    def post(self,request):
        name = request.POST.get('category','')
        if name:
            category = Category()
            category.name = name
            category.save()
            f1 = {'status': 'success', 'msg': '添加成功'}
            return HttpResponse(json.dumps(f1), content_type='application/json')
        f1 = {'status': 'fail', 'msg': '添加失败'}
        return HttpResponse(json.dumps(f1), content_type='application/json')


class ArticleModifyView(LoginRequiredMixin,View):
    '''修改文章页'''

    def get(self,request,article_id):
        # 判断用户是否登录
        # if not request.user.is_authenticated:
        #     f = {'status': 'fail', 'msg': '用户未登录'}
        #     return HttpResponse(json.dumps(f), content_type='application/json')

        article_edit = Article.objects.get(id=int(article_id))
        return render(request,'article_modify.html',{'article_edit':article_edit})

    def post(self,request,article_id):
        # 判断用户是否登录
        # if not request.user.is_authenticated:
        #     f = {'status': 'fail', 'msg': '用户未登录'}
        #     return HttpResponse(json.dumps(f), content_type='application/json')

        article = Article.objects.get(id=article_id)
        #判断用户是否为admin， 再判断是否是本文章用户
        if request.user.username != 'admin':
            if request.user.username != article.user.username:
                f = {'status': 'fail', 'msg': '你没有权限修改此文章'}
                return HttpResponse(json.dumps(f), content_type='application/json')

        article.title = request.POST.get('title', '')
        article.desc = request.POST.get('desc', '')
        article.content = request.POST.get('content', '')
        article.save()

        f1 = {'status': 'success'}
        return HttpResponse(json.dumps(f1), content_type='application/json')


class ArticleDelView(LoginRequiredMixin,View):
    '''删除文章'''

    def post(self,request,article_id):
        # 判断用户是否登录
        # if not request.user.is_authenticated:
        #     f = {'status': 'fail', 'msg': '用户未登录'}
        #     return HttpResponse(json.dumps(f), content_type='application/json')

        article = Article.objects.get(id=article_id)
        # 判断用户是否为admin， 再判断是否是本文章用户
        if request.user.username != 'admin':
            if request.user.username != article.user.username:
                f = {'status': 'fail', 'msg': '你没有权限删除此文章'}
                return HttpResponse(json.dumps(f), content_type='application/json')

        article_comments = ArticleComments.objects.filter(article=article_id) #文章删除的同时 删除有关的 评论和文章收藏
        article_comments.delete()
        art_fav = UserFav.objects.filter(fav_id=article_id)
        art_fav.delete()

        article.delete()


        f1 = {'status': 'success','msg':'删除成功!'}
        return HttpResponse(json.dumps(f1), content_type='application/json')


class ArticleCommentAddView(View):
    '''发表课程评论  将评论保持到数据库'''

    def post(self,request):
        comment_art_id = request.POST.get('art_id',0)
        comment_content = request.POST.get('art_comm_content','')

        if int(comment_art_id)>0 and comment_content:
            article_comment = ArticleComments()
            article = Article.objects.get(id=int(comment_art_id))

            article_comment.user = request.user
            article_comment.article = article
            article_comment.comments = comment_content
            article_comment.save()

            f = {'status': 'success', 'msg': '添加成功'}
            return HttpResponse(json.dumps(f), content_type='application/json')
        else:
            f = {'status': 'fail', 'msg': '添加失败'}
            return HttpResponse(json.dumps(f), content_type='application/json')


class ArticleCommentListView(View):
    '''文章评论列表'''

    def get(self,request,article_id):
        #先判断article_id,如果是0, 取出所有评论的前60条,,不是0 取出该文章的所有评论
        if int(article_id) == 0:
            all_comments = ArticleComments.objects.all().order_by('-add_time')[:60]  #默认取出最新60条评论
            all_users = Users.objects.all()

            try:
                page = request.GET.get('page', 1)
            except PageNotAnInteger:
                page = 1
            p = Paginator(all_comments, 3, request=request)  # 第二个参数表示每页显示的个数
            comments = p.page(page)

            return render(request, 'manage_comments_text.html', {
                'comments': comments,
                'article_id': article_id,
                'all_users':all_users,
            })

        article = Article.objects.get(id=article_id)
        all_comments = ArticleComments.objects.filter(article_id=int(article_id)).order_by('-add_time')
        all_users = Users.objects.all()

        try:   # 分页显示
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_comments, 10, request=request)  # 第二个参数表示每页显示的个数
        comments = p.page(page)

        return render(request,'manage_comments_text.html',{
            'comments': comments,
            'article_id': article_id,
            'article':article,
            'all_users': all_users,
        })


class ArticleCommentDelView(LoginRequiredMixin,View):
    '''删除文章评论'''

    def post(self, request, comment_id):
        # 判断用户是否登录
        # if not request.user.is_authenticated:
        #     f = {'status': 'fail', 'msg': '用户未登录'}
        #     return HttpResponse(json.dumps(f), content_type='application/json')

        comment = ArticleComments.objects.get(id=int(comment_id))
        # 判断用户是否为admin， 再判断是否是本评论用户
        if request.user.username != 'admin':
            if request.user.username != comment.user.username:
                f = {'status': 'fail', 'msg': '你没有权限删除此评论'}
                return HttpResponse(json.dumps(f), content_type='application/json')

        comment.delete()
        f1 = {'status': 'success', 'msg': '删除成功!'}
        return HttpResponse(json.dumps(f1), content_type='application/json')


class ReplyCommentView(LoginRequiredMixin,View):
    '''回复评论 回复回复'''

    def post(self, request):
        # if not request.user.is_authenticated:
        #     f = {'status': 'fail', 'msg': '用户未登录'}
        #     return HttpResponse(json.dumps(f), content_type='application/json')

        comment_id = request.POST.get('comment_id', 0)   #回复的 回复评论的ID
        reply_id = request.POST.get('reply_id',0)        #回复的 目标评论的ID或目标回复的ID
        reply_type = request.POST.get('reply_type',0)    #回复的类型 1:回复评论   2:回复回复
        to_user_id = request.POST.get('to_user_id',0)    #回复的 目标评论或回复 的用户
        # user_id = request.POST.get('user_id',0)          #回复 该评论或回复 的用户
        user_id = request.user.id                        # 回复 该评论或回复 的用户
        comment_content = request.POST.get('art_comm_content', '')  #回复内容

        if int(comment_id) > 0 and int(reply_id)>0 and int(reply_type)>0 and int(to_user_id)> 0 and comment_content:

            this_comment = ArticleReplyComments() #实例化
            comment_id1 = ArticleComments.objects.get(id= comment_id)
            to_user_id1 = Users.objects.get(id=to_user_id)

            this_comment.comment_id = comment_id1
            this_comment.reply_id = reply_id
            this_comment.reply_type = reply_type
            this_comment.to_user = to_user_id1
            this_comment.user = user_id
            this_comment.comments = comment_content
            this_comment.save()

            f = {'status': 'success', 'msg': '添加成功'}
            return HttpResponse(json.dumps(f), content_type='application/json')
        else:
            f = {'status': 'fail', 'msg': '添加失败'}
            return HttpResponse(json.dumps(f), content_type='application/json')





    # def post(self, request):
    #     comment_id = request.POST.get('comment_id', 0)
    #     comment_content = request.POST.get('art_comm_content', '')
    #
    #     if int(comment_id) > 0 and comment_content:
    #
    #         this_comment = ArticleReplyComments()
    #         # father_comment = ArticleComments.objects.get(id=int(comment_id))
    #         this_comment.comment_id = comment_id
    #         this_comment.user = request.user
    #         this_comment.comments = comment_content
    #         this_comment.save()
    #
    #         f = {'status': 'success', 'msg': '添加成功'}
    #         return HttpResponse(json.dumps(f), content_type='application/json')
    #     else:
    #         f = {'status': 'fail', 'msg': '添加失败'}
    #         return HttpResponse(json.dumps(f), content_type='application/json')














    
