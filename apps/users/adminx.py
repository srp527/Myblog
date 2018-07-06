# -*- coding:utf-8 -*- 
__author__ = 'SRP'
__date__ = '2018/5/5 14:43'

import xadmin
from xadmin import views
from xadmin.plugins.auth import UserAdmin

from .models import Users


class BaseSetting(object):# 创建xadmin的最基本管理器配置，并与view绑定
    enable_themes = True  # 开启主题功能
    use_bootswatch = True


class GlobalSettings(object): # 全局修改，固定写法
    site_title = '博客后台管理系统'
    site_footer = 'SRP-博客网站'

    menu_style = 'accordion'


xadmin.site.register(views.BaseAdminView,BaseSetting)
xadmin.site.register(views.CommAdminView,GlobalSettings)
