#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  @CreateTime    : 2018/11/20 14:43
#  @Author  : yanwj
#  @File    : test1.py


from Tools.db_tools.mongo_tools import MongoClientTools

accounts = ['meifang-club', 'gh_94e1582c5106', 'gxsp88', 'laobing157', 'sogaad', 'onelight01', 'number1_sentry', 'rshijie', 'liepinmishu', 'invre8', 'bbbbysao', 'funs360', 'zisedegu66', 'abcweiketang', 'sdyeting2016', 'sannong6', 'zhanluezongheng', 'mygtxia', 'sex-soul', 'fuxingcom', 'dianbing81', 'cssstock', 'chenghongcaijing']
conn = MongoClientTools()
data1 = conn.search('WeChat_OffiAccot_Rank')
for item in data1:
    for i in range(len(item['详情']['datas'])):
        if item['详情']['datas'][i]['account'] in accounts:
            print(item['_id'], i)


data2 = conn.search('WeChat_OffiAccot_Tag')
for item2 in data2:
    for i in range(len(item2['基本信息']['result'])):
        if item2['基本信息']['result'][i]['accountLower'] in accounts:
            print(item2['_id'], i)