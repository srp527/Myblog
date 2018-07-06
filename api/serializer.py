# -*- coding:utf-8 -*- 
__author__ = 'SRP'

'''序列化文件'''

from rest_framework import serializers
# from django.contrib.auth.models import User
# from django.forms import widgets

from blogarticle.models import Article
from users.models import Users


class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    # highlight = serializers.HyperlinkedIdentityField(view_name='snippet-highlight', format='html') #高亮显示
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Article
        # fields = '__all__'
        fields = ('id','title','desc','content','user','category','add_time')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    # articles = serializers.HyperlinkedRelatedField(many=True,view_name='article-detail',read_only=True)
    articles = ArticleSerializer(many=True,read_only=True)

    class Meta:
        model = Users
        # fields = '__all__'
        fields = ('id','username','email','add_time','articles')



