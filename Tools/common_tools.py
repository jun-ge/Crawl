#!/usr/bin/env python
# -*- coding: utf-8 -*-
#   @CreateTime    : 2018/11/20 19:02
#   @Author  : yanwj
#   @File    : common_tools.py
from Tools.db_tools.redis_tools import RedisConnection

redis_conn = RedisConnection().redis_connect()

def convert_to_dict(data):
    if isinstance(data, bytes):
        return data.decode('ascii')
    if isinstance(data, dict):
        return dict(map(convert_to_dict, data.items()))
    if isinstance(data, tuple):
        return map(convert_to_dict, data)
    return data
s = redis_conn.spop('newrank_request_item')

print(eval(s))
print(type(eval(s)))