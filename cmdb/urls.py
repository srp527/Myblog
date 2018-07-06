# -*- coding:utf-8 -*- 
__author__ = 'SRP'

from django.urls import path

from cmdb import views

app_name = 'cmdb'

urlpatterns = [
    path('login/', views.LoginView.as_view(),name='login'),
    path('logout/', views.LogoutView.as_view(),name='logout'),
    path('', views.IndexView.as_view(),name='index'),
    path('cmdb/', views.CmdbView.as_view(),name='cmdb'),
    path('assets/', views.AssetListView.as_view(),name='assets_list'),
    path('asset/', views.AssetJsonView.as_view(),name='asset_json'),
    path('asset-<device_type_id>-<asset_nid>/', views.AssetDetailView.as_view(),name='asset_detail'),
    path('add-asset/', views.AddAssetView.as_view(),name='add_asset'),

    path('users/', views.UserListView.as_view(),name='users_list'),
    path('user/', views.UserJsonView.as_view(),name='user_json'),

    path('chart-<chart_type>/', views.ChartView.as_view(),name='chart'),
]
