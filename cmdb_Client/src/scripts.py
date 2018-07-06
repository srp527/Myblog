#!/usr/bin/env python
# -*- coding:utf-8 -*-
from cmdb_Client.src.client import AutoAgent
from cmdb_Client.src.client import AutoSSH
from cmdb_Client.src.client import AutoSalt
from cmdb_Client.config import settings


def client():
    if settings.MODE == 'agent':
        cli = AutoAgent()
    elif settings.MODE == 'ssh':
        cli = AutoSSH()
    elif settings.MODE == 'salt':
        cli = AutoSalt()
    else:
        raise Exception('请配置资产采集模式，如：ssh、agent、salt')
    print('1.scripts')
    cli.process()