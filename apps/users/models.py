#-*- coding:utf-8 -*-
from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser


class Users(AbstractUser):
    nick_name = models.CharField(max_length=100,verbose_name='昵称',default='',null=True,blank=True)
    birday = models.DateField(verbose_name='生日',null=True,blank=True)
    gender = models.CharField(max_length=6,
                              choices=(('male','男'),('female','女')),default='')
    address = models.CharField(max_length=100,default='',null=True,blank=True)
    mobile = models.CharField(max_length=11, null=True, blank=True)
    image = models.ImageField(upload_to='image/%Y/%m', default='image/default.png', null=True,blank=True,max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    # def get_all_articles(self):      #取出该用户所有的文章
    #     return self.articles_set.all()

    def getToUserReplyComments(self): #根据用户评论id 反取出该用户的评论回复
        return self.articlereplycomments_set.all()

    def getUserComments(self):
        return self.articlecomments_set.all()

    def __str__(self):
        return self.username

class EmailVerifyRecord(models.Model):  # 邮箱验证码
    code = models.CharField(max_length=20, verbose_name=u'验证码')
    email = models.EmailField(max_length=50, verbose_name=u'邮箱')
    send_type = models.CharField(choices=(('register', u'注册'), ('forget', u'找回密码'), ('update_email', u'修改邮箱')),
                                     max_length=20, verbose_name=u'验证码类型')
    # 注意： now()去掉括号才会根据class实例化的时间来生成时间
    send_time = models.DateTimeField(default=datetime.now, verbose_name=u'发送时间')

    class Meta:
        verbose_name = u'邮箱验证码'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0}({1})'.format(self.code, self.email)

