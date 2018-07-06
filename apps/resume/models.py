# -*- coding:utf-8 -*-
from django.db import models

# Create your models here.


class MyResume(models.Model):
    name = models.CharField(max_length=100, verbose_name='姓名', default='', null=True, blank=True)
    birday = models.DateField(verbose_name='生日', null=True, blank=True)
    gender = models.CharField(max_length=6,
                              choices=(('male', '男'), ('female', '女')), default='')
    address = models.CharField(max_length=100, default='', null=True, blank=True)
    mobile = models.CharField(max_length=11, null=True, blank=True)
    image = models.ImageField(upload_to='image/resume', default='image/default.png', max_length=100)

    # add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')