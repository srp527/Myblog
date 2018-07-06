# -*- coding:utf-8 -*- 
__author__ = 'SRP'

from django.urls import path,include
from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view

# from rest_framework.urlpatterns import format_suffix_patterns
# from rest_framework import renderers
# from rest_framework import routers

from .views import UserViewSet,ArticleViewSet,AssetView,asset

router = DefaultRouter()
router.register('users',UserViewSet)
router.register('articles',ArticleViewSet)

schema_view = get_schema_view(title='Pastebin API')  #添加一个模式

app_name = 'apii'

urlpatterns = [
    path('',include(router.urls)),
    path('schema/',schema_view),
    path('asset/',AssetView.as_view()),
    # path('asset1/',asset),
]



###################################################
# user_list = UserViewSet.as_view({
#     'get': 'list'
# })
# user_detail = UserViewSet.as_view({
#     'get': 'retrieve'
# })
# article_list = ArticleViewSet.as_view({
#     'get': 'list',
#     'post': 'create'
# })
# article_detail = ArticleViewSet.as_view({
#     'get': 'retrieve',
#     'put': 'update',
#     'patch': 'partial_update',
#     'delete': 'destroy'
# })
#
# app_name = 'apii'
#
# # API endpoints
# urlpatterns = format_suffix_patterns([
#     path('',api_root),
#     path('users/', user_list.as_view(),name='user-list'),
#     path('user/<pk>', user_detail.as_view(),name='user-detail'),
#     path('articles/', article_list.as_view(),name='article-list'),
#     path('article/<pk>', article_detail.as_view(),name='article-detail'),
#
# ])






# from .views import UserView,ArticleView

# router = routers.DefaultRouter()
#
# router.register('users',UserView)
# router.register('articles',ArticleView)