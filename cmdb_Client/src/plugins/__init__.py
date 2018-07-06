#!/usr/bin/env python
# -*- coding:utf-8 -*-
from cmdb_Client.src.plugins.basic import BasicPlugin
from cmdb_Client.config import settings
import importlib


def get_server_info(hostname=None):
    """
    获取服务器基本信息
    :param hostname: agent模式时，hostname为空；salt或ssh模式时，hostname表示要连接的远程服务器
    :return:
    """
    print('3.plugins.__init__ get_server_info()')
    response = BasicPlugin(hostname).execute()
    if not response.status:
        return response
    print('5.plugins.__init__  循环遍历 获取cpu,硬盘,内存,主板,网卡信息')
    for k, v in settings.PLUGINS_DICT.items():
        module_path, cls_name = v.rsplit('.', 1)
        # print(module_path,cls_name)
        cls = getattr(importlib.import_module(module_path), cls_name)

        obj = cls(hostname).execute()   #obj = <cmdb_Client.lib.response.BaseResponse object at 0x00C290F0>
        # print(k,obj)
        response.data[k] = obj
    print('6.plugins完毕')
    return response


if __name__ == '__main__':
    ret = get_server_info()
    # print(ret.__dict__)