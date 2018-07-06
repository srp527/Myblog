#-*- coding:utf-8 -*-
from datetime import datetime

from django.db import models

from users.models import Users
from blogarticle.models import Article
# Create your models here.


class ArticleComments(models.Model):

    user = models.ForeignKey(Users,verbose_name='用户',on_delete=models.CASCADE) #发表评论的用户
    article = models.ForeignKey(Article,verbose_name='博客文章',on_delete=models.CASCADE,null=True,blank=True)
    comments = models.CharField(max_length=300, verbose_name=u'评论')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')
    # comment_id = models.IntegerField(verbose_name='评论目标id',default=0,null=True,blank=True)

    class Meta:
        verbose_name = u'文章评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '(%s)%s'%(self.article.title,self.comments)

    def getReplyComment(self):
        return self.articlereplycomments_set.all()
    getReplyComment.short_description = '评论回复'


class ArticleReplyComments(models.Model):

    comment_id = models.ForeignKey(ArticleComments,verbose_name='评论id',on_delete=models.CASCADE )
    reply_id = models.IntegerField(verbose_name='回复目标id',default=0)
    reply_type = models.CharField(verbose_name=u'回复类型',choices=(('1','回复评论'),('2','回复回复')),max_length=4,default=1)
    to_user = models.ForeignKey(Users, verbose_name='目标用户ID', on_delete=models.CASCADE)
    user = models.IntegerField(verbose_name='用户ID',default=0)
    comments = models.CharField(max_length=300, verbose_name=u'评论')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'评论回复'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '(%s)%s'%(self.comment_id,self.comments)


class UserFav(models.Model):
    user = models.ForeignKey(Users, verbose_name=u'用户', on_delete=models.CASCADE )
    fav_id = models.IntegerField(default=0, verbose_name=u'数据id')
    fav_type = models.IntegerField(choices=((1, '文章'), (2, '文章作者')), default=1, verbose_name=u'收藏类型')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'用户收藏'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.username