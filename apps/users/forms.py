# -*- coding:utf-8 -*- 
__author__ = 'SRP'
__date__ = '2018/5/4 20:52'

from django import forms

from .models import Users


class LoginForm(forms.Form):
    email = forms.CharField(required=True)
    passwd = forms.CharField(required=True,min_length=5)


class RegisterForm(forms.Form):
    name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    password1 = forms.CharField(required=True,min_length=5)
    password2 = forms.CharField(required=True,min_length=5)


class UploadImageForm(forms.ModelForm):

    class Meta:
        model = Users
        fields = ['image']


class UserInfoForm(forms.ModelForm):

    class Meta:
        model = Users
        fields = ['nick_name','gender','birday','address','mobile']


class ModifyPwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=5)
    password2 = forms.CharField(required=True, min_length=5)


# class ModifyEmailForm(forms.Form):
#     email = forms.EmailField(required=True)
