from django.shortcuts import render

# Create your views here.

from django.views import View
from django.shortcuts import render
from django.http import JsonResponse,HttpResponse

import json
from django.http import HttpResponse


from cmdb.service import asset,chart,user


class LoginView(View):
    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        pass


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        pass


class AssetListView(View):
    def get(self, request):

        # return render(request, 'cmdb/asset_list_text.html')
        return render(request, 'cmdb/asset_list.html')


class AssetJsonView(View):

    def get(self, request):
        obj = asset.Asset()
        response = obj.fetch_assets(request)
        return JsonResponse(response.__dict__)

        # table_config = [
        #     {
        #         'q': None,
        #         'title': '选项',
        #         'display': True,
        #         'text': {'content':"<input type='checkbox'/>",'kwargs':{}},  # 页面显示的文本 <td>内容
        #
        #     },
        #     {
        #         'q': 'id',
        #         'title': 'ID',
        #         'display': False,
        #         'text': {},  #页面显示的文本 <td>内容
        #
        #     },
        #     {
        #         'q': 'idc__name',
        #         'title': '机房名',
        #         'display': True,
        #         'text': {'content':'{n}', 'kwargs':{'n':'@idc__name'}},
        #         'attrs': {'edit-enable':'true', 'edit-type':'input'}
        #     },
        #     {
        #         'q': 'cabinet_num',
        #         'title': '机柜号',
        #         'display': True,
        #         'text': {'content': '{n}', 'kwargs': {'n': '@cabinet_num'}},
        #         'attrs': {'edit-enable':'true', 'edit-type':'input'}
        #     },
        #     {
        #         'q': 'cabinet_order',
        #         'title': '机柜中序号',
        #         'display': True,
        #         'text': {'content': '{n}', 'kwargs': {'n': '@cabinet_order'}},
        #         'attrs': {'edit-enable':'true', 'edit-type':'input'}
        #     },
        #     {
        #         'q': 'device_type_id',
        #         'title': "资产类型",
        #         'display': 1,
        #         'text': {'content': "{n}", 'kwargs': {'n': '@@device_type_choices'}},
        #         'attrs': {'edit-enable':'true','edit-type':'select'}
        #     },
        #     {
        #         'q': 'device_status_id',
        #         'title': "资产状态",
        #         'display': 1,
        #         'text': {'content': "{n}", 'kwargs': {'n': '@@device_status_choices'}},
        #         'attrs': {'edit-enable':'true','edit-type':'select'}
        #     },
        #     {
        #         'q': None,
        #         'title': '操作',
        #         'display': True,
        #         'text': {'content': '<a href="/cmdb/asset-{m}-{n}/">查看详情</a>', 'kwargs': {'m':'@device_type_id','n':'@id'}},
        #         'attrs':{}
        #     },
        #     # {
        #     #     'q': 'server_title',
        #     #     'title': "主机名",
        #     #     'display': 1,
        #     #     'text': {'content': "{n}", 'kwargs': {'n': '@server_title'}},
        #     #     'attr': {}
        #     # },
        # ]
        # q_list = [i['q'] for i in table_config if i['q'] is not None]
        # print('q_list', q_list)
        # from cmdb import models
        #
        # data_list = models.Asset.objects.all().values(*q_list)
        # data_list = list(data_list)
        #
        # result = {
        #     'table_config':table_config,
        #     'data_list':data_list,
        #     'global_dict':{     #前端的全局变量
        #         'device_type_choices': models.Asset.device_type_choices,
        #         'device_status_choices':models.Asset.device_status_choices,
        #     },
        # }
        # return HttpResponse(json.dumps(result))


    def delete(self, request):
        response = asset.Asset.delete_assets(request)
        return JsonResponse(response.__dict__)

    def put(self, request):
        response = asset.Asset.put_assets(request)
        return JsonResponse(response.__dict__)


class AssetDetailView(View):
    def get(self, request, device_type_id, asset_nid):
        response = asset.Asset.assets_detail(device_type_id, asset_nid)
        return render(request, 'cmdb/asset_detail.html', {'response': response, 'device_type_id': device_type_id})


class AddAssetView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'cmdb/add_asset.html')


class IndexView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'cmdb/index.html')


class CmdbView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'cmdb/cmdb.html')


class ChartView(View):
    def get(self, request, chart_type):
        if chart_type == 'business':
            response = chart.Business.chart()
        if chart_type == 'dynamic':
            last_id = request.GET.get('last_id')
            response = chart.Dynamic.chart(last_id)

        return JsonResponse(response.__dict__, safe=False, json_dumps_params={'ensure_ascii': False})


class UserListView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'cmdb/users_list.html')


class UserJsonView(View):
    def get(self, request):
        obj = user.User()
        response = obj.fetch_users(request)
        return JsonResponse(response.__dict__)

    def delete(self, request):
        response = user.User.delete_users(request)
        return JsonResponse(response.__dict__)

    def put(self, request):
        response = user.User.put_users(request)
        return JsonResponse(response.__dict__)

