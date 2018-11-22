#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import time
import logging
from pymongo import MongoClient, errors

from config import CONFIG_MONGO


class MongoConnection(object):
    def __init__(self):
        self.logger = logging.getLogger('MongoConnection')

    def mongo_conn(self, **kwargs):
        while True:
            try:
                if kwargs.get('url', None):
                    return MongoClient(kwargs.get('url'))[kwargs.get('db')]
                else:
                    return MongoClient(CONFIG_MONGO['url'])[CONFIG_MONGO['db2']]
            except errors.PyMongoError as e:
                self.logger.error("mongodb_conn链接失败,reconnect,error_msg:{}".format(e))
                time.sleep(3)
                continue


class MongoClientTools(object):
    def __init__(self, **kwargs):
        self.logger = logging.getLogger('MongoClientTools')
        self.__conn = MongoConnection().mongo_conn(**kwargs)

    def save(self, dict_data, table_name, find=None, many=False):
        '''

        :param dict_data: 字典类型数据
        :param table_name: 表明
        :param find: 条件
        :param many: 是否存入多条
        :return: None
        '''
        try:
            if find:
                if getattr(self.__conn, table_name).find(find).count():
                    if many:
                        getattr(self.__conn, table_name).update_many(find, dict_data)
                    else:
                        getattr(self.__conn, table_name).update(find, dict_data)
                else:
                    self.logger.debug('匹配字段:{}无法查询到 %s, 插入新数据' % find)
                    getattr(self.__conn, table_name).insert(dict_data)
            else:
                getattr(self.__conn, table_name).insert(dict_data)
        except Exception as e:
            self.logger.error('data:{}, error_msg:{}'.format(str(dict_data), e))

    def search(self, table_name, find=None, sorted_key=None, reverse=False, limit=None):
        try:
            if isinstance(find, dict):
                if limit:
                    return getattr(self.__conn, table_name).find(find).sort({sorted_key: 1}).limit(limit) if not reverse \
                        else getattr(self.__conn, table_name).find(find).sort({sorted_key: -1}).limit(limit)
                else:
                    if sorted_key:
                        return getattr(self.__conn, table_name).find(find).sort(
                            {sorted_key: 1}) if not reverse else getattr(
                            self.__conn, table_name).find(find).sort({sorted_key: -1})
                    else:
                        return getattr(self.__conn, table_name).find(find)
            elif isinstance(find, str):
                return getattr(self.__conn, table_name).distinct(find)
            else:
                return getattr(self.__conn, table_name).find(find)
        except Exception as e:
            self.logger.error('search from key:{}, error_msg:{}'.format(str(find), e))

    def delete(self, table_name, find, many=True):
        """
        # mongodb客户端删除重复数据操作代码
        db.getCollection('数据表名称').aggregate([
            {
                $group:{_id:{字段名:'$字段名'}, count:{$sum:1}, dups:{$addToSet: '$_id'}}
            },
            {
                $match:{count:{$gt:1}}
            }
        ]).forEach(function(doc){
                doc.dups.shift();
                db.getCollection('数据表名称').remove({_id: {$in: doc.dups}});
            })

        删除一条或多条数据
        :param table_name:
        :param find: 删除对象的key
        :param many: many 为True删除多个
        :return: A cursor / iterator over Mongo query results.
        """
        try:
            if many:
                getattr(self.__conn, table_name).delete_many(find)
            else:
                getattr(self.__conn, table_name).delete_one(find)
        except Exception as e:
            self.logger.error('search from key:{}, error_msg:{}'.format(str(find), e))


if __name__ == '__main__':
    conn = MongoClientTools(url='mongodb://127.0.0.1:62178', db='盐行业(诚信数据)')
    for item in conn.search('盐行业不良名单', {}):
        print(item)
