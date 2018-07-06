# -*- coding:utf-8 -*- 
__author__ = 'SRP'
__date__ = '2018/5/5 16:07'

import xadmin

from.models import ArticleComments,ArticleReplyComments


class ArticleCommentsAdmin(object):

    list_display = ['user','article','comments','add_time']
    search_fields = ['user','article','comments']
    list_filter = ['user','article','comments','add_time']


class ReplyCommentAdmin(object):
    list_display = ['user', 'comment_id', 'comments', 'add_time']
    search_fields = ['user', 'comment_id', 'comments']
    list_filter = ['user', 'comment_id', 'comments', 'add_time']


xadmin.site.register(ArticleComments,ArticleCommentsAdmin)
xadmin.site.register(ArticleReplyComments,ReplyCommentAdmin)