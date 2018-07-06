#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os

BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 用于API认证的KEY
KEY = '299095cc-1330-11e5-b06a-a45e60bec08b'
# 用于API认证的请求头
AUTH_KEY_NAME = 'auth-key'

# 错误日志
ERROR_LOG_FILE = os.path.join(BASEDIR, "log", 'error.log')
# 运行日志
RUN_LOG_FILE = os.path.join(BASEDIR, "log", 'run.log')

# Agent模式保存服务器唯一ID的文件
CERT_FILE_PATH = os.path.join(BASEDIR, 'config', 'cert')

# 是否测试模式，测试模时候数据从files目录下读取
TEST_MODE = False

# 采集资产的方式，选项有：agent(默认), salt, ssh
# MODE = 'agent'
MODE = 'ssh'

# 如果采用SSH方式，则需要配置SSH的KEY和USER
# SSH_PRIVATE_KEY = "/home/auto/.ssh/id_rsa"
SSH_PRIVATE_KEY = os.path.join(BASEDIR,'config','key','192.168.30.11')
SSH_USER = "root"
SSH_PORT = 22

# 采集硬件数据的插件
PLUGINS_DICT = {
    'cpu': 'cmdb_Client.src.plugins.cpu.CpuPlugin',
    'disk': 'cmdb_Client.src.plugins.disk.DiskPlugin',
    'main_board': 'cmdb_Client.src.plugins.main_board.MainBoardPlugin',
    'memory': 'cmdb_Client.src.plugins.memory.MemoryPlugin',
    'nic': 'cmdb_Client.src.plugins.nic.NicPlugin',
}

# 资产信息API
ASSET_API = "http://127.0.0.1:8000/api/asset/"
"""
POST时，返回值：{'code': xx, 'message': 'xx'}
 code:
    - 1000 成功;
    - 1001 接口授权失败;
    - 1002 数据库中资产不存在
"""
if __name__ == '__main__':
    print(BASEDIR)