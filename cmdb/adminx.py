# -*- coding:utf-8 -*- 
__author__ = 'SRP'

import xadmin
from .models import UserProfile,AdminInfo,UserGroup,BusinessUnit,IDC,Tag,AssetRecord
from .models import Asset,Server,NetworkDevice,Disk,NIC,Memory,ErrorLog

# class ArticleAdmin(object):
#
#     list_display = ['title','user','desc','content','category','add_time']
#     search_fields = ['title','user','desc','content','category']
#     list_filter = ['title','desc','content','category','user','add_time']
#
#     style_fields = {'content': 'ueditor'}
#     import_excel = True

xadmin.site.register(UserProfile)
xadmin.site.register(AdminInfo)
xadmin.site.register(UserGroup)
xadmin.site.register(BusinessUnit)
xadmin.site.register(Asset)
xadmin.site.register(Server)
xadmin.site.register(NetworkDevice)
xadmin.site.register(Disk)
xadmin.site.register(NIC)
xadmin.site.register(Memory)
xadmin.site.register(IDC)
xadmin.site.register(Tag)
xadmin.site.register(AssetRecord)
xadmin.site.register(ErrorLog)