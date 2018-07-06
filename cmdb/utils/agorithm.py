#!/usr/bin/env python
# -*- coding:utf-8 -*-


def get_intersection(*args):
    '''
    获取所有set的交集
    :param args: set集合
    :return:交集列表
    '''
    base = args[0]
    result = base.intersection(*args)
    return list(result)



def get_exclude(total,part):
    result = []
    for item in total:
        if item in part:
            pass
        else:
            result.append(item)
    return result

if __name__ == '__main__':
    a1 = {1,2,3,4,5}
    a2 = {2,3,4,5,6,7}
    new = get_intersection(a2,a1)
    new1 = get_exclude(a1,a2)
    print(new1)
