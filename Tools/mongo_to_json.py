#!/usr/bin/env python
# -*- coding: utf-8 -*-
#   @CreateTime    : 2018/11/19 16:13
#   @Author  : yanwj
#   @File    : mongo_to_json.py


import datetime
import json

from Tools.db_tools.mongo_tools import MongoClientTools


# 使json能够转化datetime对象
class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)


def convert(dic_data):
    # 对于引用的Id和该条数据的Id，这里都是ObjectId类型的
    from bson import ObjectId
    # 字典遍历
    for key, value in dic_data.items():
        # 如果是列表，则递归将值清洗
        if isinstance(value, list):
            for l in value:
                convert(l)
        else:
            if isinstance(value, ObjectId):
                dic_data[key] = str(dic_data.pop(key))
    return dic_data


if __name__ == '__main__':
    conn = MongoClientTools()
    index = 0
    dict_data = {}
    data = conn.search('WeChat_OffiAccot_Info')
    with open('WeChat_OffiAccot_info.json', 'w', encoding='UTF-8') as fw:
        for item in data:
            dict_data[index] = convert(item)
            index += 1
        fw.write(json.dumps(dict_data, cls=DateEncoder, ensure_ascii=False))
