# -*- coding:utf-8 -*- 
__author__ = 'SRP'
__date__ = '2018/5/4 17:23'

from django.urls import path

from .views import ArticleView,ArticleListView,ArticleAddView,ArticleModifyView,ArticleDelView
from .views import ArticleCommentAddView,ArticleCommentListView,ArticleCommentDelView,ReplyCommentView
from .views import AddCategoryView

app_name = 'blog'
urlpatterns = [

    path('article_detail/<article_id>', ArticleView.as_view(),name='article_detail'),
    path('article_list/', ArticleListView.as_view(),name='article_list'),
    path('article_add/', ArticleAddView.as_view(),name='article_add'),
    path('article_modify/<article_id>', ArticleModifyView.as_view(),name='article_modify'),
    path('article_del/<article_id>', ArticleDelView.as_view(),name='article_del'),
    path('article_comment/', ArticleCommentAddView.as_view(),name='article_comment_add'),
    path('article_comment_list/<article_id>', ArticleCommentListView.as_view(),name='article_comment_list'),
    path('article_comment_del/<comment_id>', ArticleCommentDelView.as_view(),name='article_comment_del'),
    path('article_reply_comment_add/', ReplyCommentView.as_view(),name='article_reply_comment_add'),
    path('article_category_add/', AddCategoryView.as_view(),name='article_category_add'),
  ]