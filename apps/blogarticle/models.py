# -*- coding:utf-8 -*-

from datetime import datetime

from django.db import models
from DjangoUeditor.models import UEditorField

from users.models import Users
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=150,unique=True,verbose_name='类别名称')
    add_time = models.DateTimeField(auto_now_add=True)


class Article(models.Model):
    user = models.ForeignKey(Users,verbose_name='文章作者',related_name='articles',null=True, blank=True,on_delete=models.CASCADE)
    category = models.CharField(max_length=20, verbose_name='文章类别', default='python基础知识')
    # category = models.ForeignKey(Category, verbose_name='文章类别', null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=50,verbose_name='文章标题')
    desc = models.CharField(max_length=300,verbose_name='文章描述')
    content = UEditorField(verbose_name='文章内容',width=600,height=300,
                           imagePath='article/ueditor/',
                           filePath='article/ueditor/', default='')
    click_nums = models.IntegerField(default=0, verbose_name=u'阅读数')
    # tag 设置一个标签，相关推荐里用到
    tag = models.CharField(default='', verbose_name=u'文章标签', max_length=20,null=True, blank=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = u'文章'
        verbose_name_plural = verbose_name

    def getArtcileComment(self):  #获取文章所有评论
        return self.articlecomments_set.all().order_by('-add_time')

    def getArtcileCommentCount(self):  #获取文章评论数
        return self.articlecomments_set.all().count()

    def __str__(self):
        return self.title


