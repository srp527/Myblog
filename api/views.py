# -*- coding:utf-8 -*- 
__author__ = 'SRP'
__date__ = '2018/6/19 18:16'

# import json
# from django.http import HttpResponse
# from rest_framework import generics
# from rest_framework.decorators import api_view  #创建端点
# from rest_framework.response import Response    #创建端点
# from rest_framework.reverse import reverse      #创建端点
# from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework import permissions,renderers

from users.models import Users
from blogarticle.models import Article
from .serializer import UserSerializer,ArticleSerializer
from .permissions import IsOwnerOrReadOnly

#############################################################################
######################### ----Blog -----#####################################
################# viewsets视图集重构 list/detail #############################
#############################################################################

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
        这个视图集自动提供list和detail动作
    """
    queryset = Users.objects.all()
    serializer_class = UserSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    """
       此视图集自动提供“列表”、“创建”、“检索”，“更新”和“删除”行动。

    """

    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        # print(self.request.user)

    # 我们这里没有用高亮显示
    # @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    # def highlight(self, request, *args, **kwargs):
    #     snippet = self.get_object()
    #     return Response(snippet.highlighted)


# @api_view(['GET'])   #为API的根创建端点
# def api_root(request,format=None):
#     if request.method == 'GET':
#         data = {
#             'users': reverse('user-list',request=request,format=format),
#             'articles': reverse('article-list',request=request,format=format),
#         }
#         return Response(data)
        # return HttpResponse(json.dumps(data),content_type='application/json')

##################################################################
########################  cmdb  ##################################
###################### 资产更新入库 ##############################
##################################################################
import json
import importlib
from django.views import View
from django.http import JsonResponse
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from cmdb.utils import auth
from api.service import config
from cmdb import models
from api.service import asset
from api.service.asset import get_untreated_servers

@csrf_exempt
@auth.api_auth
def asset(request):
    '''test'''
    pass

    # print(request.method)
    # print(request.GET)
    # print(request.POST)
    # # print(request.body)
    # import json
    # host_info = json.loads(request.body.decode('utf-8'))
    # print(host_info)
    # return HttpResponse('11111')


class AssetView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(AssetView, self).dispatch(request, *args, **kwargs)

    @method_decorator(auth.api_auth)
    def get(self, request, *args, **kwargs):
        """
        获取今日未更新的资产 - 适用SSH或Salt客户端
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # print('11111111111111')
        response = get_untreated_servers()
        print(response.__dict__)
        return JsonResponse(response.__dict__)


    @method_decorator(auth.api_auth)
    def post(self, request, *args, **kwargs):
        """
        更新或者添加资产信息
        :param request:
        :param args:
        :param kwargs:
        :return: 1000 成功;1001 接口授权失败;1002 数据库中资产不存在
        """

        server_info = json.loads(request.body.decode('utf-8'))
        server_info = json.loads(server_info)             # server_info 最新汇报服务器所有信息
        # ret = {'code': 1000, 'message': ''}
        # print(server_info)
        hostname = server_info['hostname']

        ret = {'code': 1000, 'message': '[%s]更新完成' % hostname}


        # 根据主机名去数据库中获取相关信息 ,数据库已存在的主机相关信息
        server_obj = models.Server.objects.filter(hostname=hostname).select_related('asset').first()
        if not server_obj:
            ret['code'] = 1002
            ret['message'] = '[%s]资产不存在' % hostname
            return JsonResponse(ret)

        for k, v in config.PLUGINS_DICT.items():
            module_path, cls_name = v.rsplit('.', 1)
            print('module-path | cls_name:',module_path,cls_name)

            cls = getattr(importlib.import_module(module_path), cls_name)
            response = cls.process(server_obj, server_info, None)
            print('response',response.status)
            if not response.status:
                ret['code'] = 1003
                ret['message'] = "[%s]资产更新异常" % hostname
            if hasattr(cls, 'update_last_time'):
                cls.update_last_time(server_obj, None)

        return JsonResponse(ret)


'''{
"os_platform": "linux", 
"os_version": "CentOS release 6.6 (Final)", 
"hostname": "c1.com", 
"cpu": {"cpu_count": 24, "cpu_physical_count": 2, "cpu_model": " Intel(R) Xeon(R) CPU E5-2620 v2 @ 2.10GHz"},
"disk": {"0": {"slot": "0", "pd_type": "SAS", "capacity": "279.396", "model": "SEAGATE ST300MM0006     LS08S0K2B5NV"}, "1": {"slot": "1", "pd_type": "SAS", "capacity": "279.396", "model": "SEAGATE ST300MM0006     LS08S0K2B5AH"}, "2": {"slot": "2", "pd_type": "SATA", "capacity": "476.939", "model": "S1SZNSAFA01085L     Samsung SSD 850 PRO 512GB               EXM01B6Q"}, "3": {"slot": "3", "pd_type": "SATA", "capacity": "476.939", "model": "S1AXNSAF912433K     Samsung SSD 840 PRO Series              DXM06B0Q"}, "4": {"slot": "4", "pd_type": "SATA", "capacity": "476.939", "model": "S1AXNSAF303909M     Samsung SSD 840 PRO Series              DXM05B0Q"}, "5": {"slot": "5", "pd_type": "SATA", "capacity": "476.939", "model": "S1AXNSAFB00549A     Samsung SSD 840 PRO Series              DXM06B0Q"}}, 
"main_board": {"manufacturer": "Parallels Software International Inc.", "model": "Parallels Virtual Platform", "sn": "Parallels-1A 1B CB 3B 64 66 4B 13 86 B0 86 FF 7E 2B 20 30"}, 
"memory": {"DIMM #0": {"capacity": 1024, "slot": "DIMM #0", "model": "DRAM", "speed": "667 MHz", "manufacturer": "Not Specified", "sn": "Not Specified"}, "DIMM #1": {"capacity": 0, "slot": "DIMM #1", "model": "DRAM", "speed": "667 MHz", "manufacturer": "Not Specified", "sn": "Not Specified"}, "DIMM #2": {"capacity": 0, "slot": "DIMM #2", "model": "DRAM", "speed": "667 MHz", "manufacturer": "Not Specified", "sn": "Not Specified"}, "DIMM #3": {"capacity": 0, "slot": "DIMM #3", "model": "DRAM", "speed": "667 MHz", "manufacturer": "Not Specified", "sn": "Not Specified"}, "DIMM #4": {"capacity": 0, "slot": "DIMM #4", "model": "DRAM", "speed": "667 MHz", "manufacturer": "Not Specified", "sn": "Not Specified"}, "DIMM #5": {"capacity": 0, "slot": "DIMM #5", "model": "DRAM", "speed": "667 MHz", "manufacturer": "Not Specified", "sn": "Not Specified"}, "DIMM #6": {"capacity": 0, "slot": "DIMM #6", "model": "DRAM", "speed": "667 MHz", "manufacturer": "Not Specified", "sn": "Not Specified"}, "DIMM #7": {"capacity": 0, "slot": "DIMM #7", "model": "DRAM", "speed": "667 MHz", "manufacturer": "Not Specified", "sn": "Not Specified"}}, 
"nic": {"eth0": {"up": true, "hwaddr": "00:1c:42:a5:57:7a", "ipaddrs": "10.211.55.4", "netmask": "255.255.255.0"}}}
'''
#####################################################################################
############################### 进一步整合 ######################################
#####################################################################################

# class ArticleHighlight(generics.GenericAPIView):  #高亮显示
#     queryset = Article.objects.all()
#     renderer_classes = (renderers.StaticHTMLRenderer,)
#
#     def get(self,request,*args,**kwargs):
#         article = self.get_object()
#         return Response(article.highlighted)


# class UserList(generics.ListCreateAPIView):
#     ''' get post'''
#     queryset = Users.objects.all()
#     serializer_class = UserSerializer
#
#
# class UserDetail(generics.RetrieveUpdateDestroyAPIView):
#     ''' get put delete'''
#     queryset = Users.objects.all()
#     serializer_class = UserSerializer


# class ArticleList(generics.ListCreateAPIView):
#     ''' get post'''
#     queryset = Article.objects.all()
#     serializer_class = ArticleSerializer
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
#
#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)
#
#
# class ArticleDetail(generics.RetrieveUpdateDestroyAPIView):
#     ''' get put delete'''
#     queryset = Article.objects.all()
#     serializer_class = ArticleSerializer
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,
#                           IsOwnerOrReadOnly,)




#############################################################################
##########################  类视图 APIView ##################################
#############################################################################
# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.views import APIView
#
# from users.models import Users
# from blogarticle.models import Article
# from .serializer import UserSerializer,ArticleSerializer
#
#
# class UserList(APIView):
#     def get(self,request,format=None):
#         queryset = Users.objects.all()
#         serializer = UserSerializer(queryset,many=True)
#         # return HttpResponse(json.dumps(serializer.data),content_type='application/json')
#         return Response(serializer.data)
#     def post(self,request,format=None):
#         data = request.data
#         serializer = UserSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_201_CREATED)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
#
#
# class UserDetail(APIView):
#     def get_obj(self,pk):
#         try:
#             return Users.objects.get(pk=pk)
#         except Exception as e:
#             pass
#
#     def get(self,request,pk,format=None):
#         user = self.get_obj(pk)
#         serializer = UserSerializer(user)
#         return Response(serializer.data)
#
#     def put(self,request,pk,format=None):
#         user = self.get_obj(pk)
#         serializer = UserSerializer(user,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self,request,pk,format=None):
#         user = self.get_obj(pk)
#         user.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

###################################################################################################
########################################  函数视图  api_view ######################################
###################################################################################################
# from rest_framework import status
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework import viewsets
# # from django_filters import rest_framework as filters
#
# from users.models import Users
# from blogarticle.models import Article
# from .serializer import UserSerializer,ArticleSerializer
#
#
# @api_view(['GET','POST'])
# def UsersView(request,format=None):
#     """
#     列出所有已经存在的 user 或者创建一个新的 user
#     """
#     if request.method == 'GET':
#         users = Users.objects.all()
#         serializer = UserSerializer(users, many=True)
#         data = serializer.data
#         return Response(data)
#
#     elif request.method == 'POST':
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# @api_view(['GET','PUT','DELETE'])
# def User_detail(request, pk,format=None):
#     """
#     检索查看、更新或者删除一个代码段
#     """
#     try:
#         user = Users.objects.get(pk=pk)
#     except Users.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == 'GET':
#         serializer = UserSerializer(user)
#         return Response(serializer.data)
#
#     elif request.method == 'PUT':
#         serializer = UserSerializer(user, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     elif request.method == 'DELETE':
#         user.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

