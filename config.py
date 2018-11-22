#!/usr/bin/env python
# -*- coding: utf-8 -*-
#   @CreateTime    : 2018/11/7 15:11
#   @Author  : yanwj
#   @File    : config.py

# env = 'online'
# env = 'test'
env = 'local'

if env == 'test':
    CONFIG_MONGO = {
        'url': 'mongodb://172.18.83.123:27018',
        'db': 'MACRO',
        'db2': 'PUBLIC',
        'table': 'macro_eco_',
        'table2': 'WeChat_OffiAccot_',
        # 跳板
        'ssh': '47.106.124.184',
        'user': 'root',
        'port':'22',
        'password': 'KAdmin@2018#'
    }
    CONFIG_REDIS = {
        'host': '172.18.33.121',
        'port': '6379',
        'password': 'KrrwuhCWVH',
        'db': 1,
    }


    PROXY_REDIS = 'http://172.18.83.126:5010/'

elif env == 'online':
    CONFIG_MONGO = {
        'url': 'mongodb://172.18.83.123:27017',
        'db': 'MACRO',
        'db2': 'PUBLIC',
        'table': 'macro_eco_',
        'table2': 'WeChat_OffiAccot_',
    }
    CONFIG_REDIS = {
        'host': '172.18.33.121',
        'port': '6379',
        'password': 'KrrwuhCWVH',
        'db': 0,
    }

    PROXY_REDIS = 'http://172.18.83.126:5010/'
elif env == 'local':
    CONFIG_MONGO = {
        'url': 'mongodb://localhost:27017',
        'db': 'MACRO',
        'db2': 'PUBLIC',
        'table': 'macro_eco_',
        'table2': 'WeChat_OffiAccot_',
        # 跳板
        'ssh': '47.106.124.184',
        'user': 'root',
        'password': 'KAdmin@2018#'
    }
    PROXY_REDIS = 'http://localhost:5010/'

    CONFIG_REDIS = {
         'host': 'localhost',
         'port': '6379',
         'password': '',
         'db': 1,
     }
