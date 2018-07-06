# -*- coding:utf-8 -*- 
__author__ = 'SRP'

import os,json
dir_path = os.path.dirname(os.path.abspath('__file__'))
file_path = os.path.join(dir_path,'disk')
print(dir_path)
with open(file_path,'r') as f :
    a = f.read()
    a = json.dumps(a)
    print(a)