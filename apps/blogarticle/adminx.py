# -*- coding:utf-8 -*- 
__author__ = 'SRP'
__date__ = '2018/5/5 14:49'

import xadmin

from .models import Article


class ArticleAdmin(object):

    list_display = ['title','user','desc','content','category','add_time']
    search_fields = ['title','user','desc','content','category']
    list_filter = ['title','desc','content','category','user','add_time']

    style_fields = {'content': 'ueditor'}
    import_excel = True


xadmin.site.register(Article,ArticleAdmin)