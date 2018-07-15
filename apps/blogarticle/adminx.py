# -*- coding:utf-8 -*- 
__author__ = 'SRP'
__date__ = '2018/5/5 14:49'

import xadmin

from .models import Article,Category


class ArticleAdmin(object):

    list_display = ['title','user','desc','content','category','add_time']
    search_fields = ['title','user','desc','content','category']
    list_filter = ['title','desc','content','category','user','add_time']

    style_fields = {'content': 'ueditor'}
    import_excel = True


class CategoryAdmin(object):
    list_display = ['name','add_time']
    search_fields = ['name']
    list_filter = ['name','add_time']


xadmin.site.register(Article,ArticleAdmin)
xadmin.site.register(Category,CategoryAdmin)