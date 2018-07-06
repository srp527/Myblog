#!/usr/bin/env python
# -*- coding:utf-8 -*-
import traceback
from .base import BasePlugin
from cmdb_Client.lib.response import BaseResponse


class BasicPlugin(BasePlugin):
    '''服务器基本信息
       系统平台,版本,主机名.'''

    def os_platform(self):
        """
        获取系统平台
        :return:
        """
        if self.test_mode:
            output = 'linux'
        else:
            output = self.exec_shell_cmd('uname')
            output = str(output, encoding='utf-8')
        return output.strip()

    def os_version(self):
        """
        获取系统版本
        :return:
        """
        if self.test_mode:
            output = """CentOS release 6.6 (Final)\nKernel \r on an \m"""
        else:
            output = self.exec_shell_cmd('cat /etc/issue')
            output = str(output,encoding='utf-8')
        result = output.strip().split('\n')[0]
        print('basic.py result' ,result )  ########################## print #############
        return result

    def os_hostname(self):
        """
        获取主机名
        :return:
        """
        if self.test_mode:
            output = 'c1.com'
        else:
            output = self.exec_shell_cmd('hostname')
            output = str(output, encoding='utf-8')
        return output.strip()

    def linux(self):
        print('4.basic,系统平台,版本,主机名')
        response = BaseResponse()
        try:
            ret = {
                'os_platform': self.os_platform(),
                'os_version': self.os_version(),
                'hostname': self.os_hostname(),
            }
            response.data = ret
            print('ret------>>',ret)
        except Exception as e:
            msg = "%s BasicPlugin Error:%s"
            self.logger.log(msg % (self.hostname, traceback.format_exc()), False)
            response.status = False
            response.error = msg % (self.hostname, traceback.format_exc())

        return response

