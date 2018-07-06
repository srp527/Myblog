# -*- coding:utf-8 -*- 
__author__ = 'SRP'
__date__ = '2018/5/4 17:23'

from django.urls import path

from .views import LoginView,LogoutView,RegisterView,UserListView
from .views import AddDelFavView,UserFavView,UserImageView,UserModifyPwdView,UserModifyEmailView,UserInfoView

app_name = 'user'
urlpatterns = [
    # path('get_article/', GetArticle.as_view(),name='get_article'),
    path('login/', LoginView.as_view(),name='login'),
    path('logout/', LogoutView.as_view(),name='logout'),
    path('register/',RegisterView.as_view(),name='register'),
    path('user_list/',UserListView.as_view(),name='user_list'),
    path('add_fav/',AddDelFavView.as_view(),name='add_fav'),
    path('user_fav/',UserFavView.as_view(),name='user_fav'),
    path('user_img/',UserImageView.as_view(),name='user_img'),
    path('user_modify_pwd/',UserModifyPwdView.as_view(),name='user_modify_pwd'),
    path('user_modify_email/',UserModifyEmailView.as_view(),name='user_modify_email'),
    path('user_info/', UserInfoView.as_view(), name='user_info'),

]