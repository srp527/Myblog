# -*- coding:utf-8 -*- 
__author__ = 'SRP'

from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    自定义权限，仅允许对象的所有者编辑它。
    """
    def has_object_permission(self, request, view, obj):
        #允许对任何请求进行读权限，
        #所以我们总是允许GET、HEAD或OPTIONS请求。
        if request.method in permissions.SAFE_METHODS:
            return True
        # 而当请求不是上面的安全模式的话，那就需要判断一下当前的用户
        # 如果Snippet所有者和当前的用户一致，那就允许，否则返回错误信息
        return obj.user == request.user