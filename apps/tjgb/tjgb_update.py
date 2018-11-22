#!/usr/bin/env python
# -*- coding: utf-8 -*-
#   @CreateTime    : 2018/11/5 16:15
#   @Author  : yanwj
#   @File    : tjgb_pro.py

# 本脚本主要是更新，文章正文内容，对于部分正文缺失的情况重新抓取，需要时启动

import logging
import os
import random
import time

import requests
from pyquery import PyQuery
import threadpool
from Tools.db_tools.mongo_tools import MongoClientTools
from Tools.http_tools import HEADERS, get_response
from config import CONFIG_MONGO
from apps.tjgb.tjgb_total import get_detail_page, get_content, RESOURCE_NAME


def get_index_page(state, state_url):
    try:
        doc = PyQuery(get_response(state_url, headers=HEADERS).content.decode('gb2312', 'ignore'))
    except Exception as e:
        logging.info('{%s}页面解析错误--》{%s} 再次尝试解析' % (e))
        doc = PyQuery(get_response(state_url, headers=HEADERS).content.decode('gb2312', 'ignore'))
    time.sleep(random.randint(1, 20) / 10)
    url_list = [li_tag('a').attr.href for li_tag in doc('.news_list  .box  li').items()]
    for url in url_list:
        bulletin = conn.search(CONFIG_MONGO['table'] + RESOURCE_NAME, {'链接': 'http://www.tjcn.org' + url})
        if bulletin.count():
            bulletin = list(bulletin)[0]
            # 如果更新次数大于三次, 或者三次都没更新过的，则不再更新,
            if bulletin.get('content_update_times', 0) > 2 or bulletin.get('content_update_times', 0) < -2:
                continue
            else:
                update_detail_content('http://www.tjcn.org' + url, bulletin)
        else:
            get_detail_page(state, url)
    if '下一页' in str(doc('.epages')):
        next_page = doc('.epages a').eq(-2).attr.href
        next_page_url = 'http://www.tjcn.org' + next_page
        get_index_page(state, next_page_url)


def update_detail_content(detail_url, bulletin):
    content = ""
    content = get_content(detail_url, content)
    exist_content = bulletin['正文']
    if len(content) > len(exist_content):
        logging.info('已有正文{%s}信息缺失，正在更新' % detail_url)
        if bulletin.get('content_update_times', None):
            conn.save({'$inc': {'content_update_times': 1}, '$set': {'正文': content}}, CONFIG_MONGO['table'] + RESOURCE_NAME, find={'链接': detail_url})
        else:
            conn.save({'$set': {'content_update_times': 1, '正文': content}}, CONFIG_MONGO['table'] + RESOURCE_NAME, find={'链接': detail_url})
    else:
        if bulletin.get('content_update_times', None):
            conn.save({'$inc': {'content_update_times': -1}}, CONFIG_MONGO['table'] + RESOURCE_NAME, find={'链接': detail_url})
        else:
            conn.save({'$set': {'content_update_times': -1}}, CONFIG_MONGO['table'] + RESOURCE_NAME, find={'链接': detail_url})
        logging.info('已有正文{%s}信息与最新爬取数据相同' % detail_url)


def main_update():
    while True:
        if not os.path.exists("./log"):
            os.makedirs("./log")
        logging.basicConfig(level=logging.INFO,
                            filemode="a",
                            filename="./log/tjgb_update.log",
                            format='%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s', )
        try:
            conn = MongoClientTools(url=CONFIG_MONGO['url'], db=CONFIG_MONGO['db'])
        except Exception as e:
            logging.info('链接数据库Error--》%s' % e)

        url = 'http://www.tjcn.org/tjgb/'
        doc = PyQuery(requests.get(url).content)
        states = {}
        a_tags = doc('.zlm a')
        for a in a_tags.items():
            states[a.text()] = 'http://www.tjcn.org' + a.attr.href
        logging.info(states)
        pool = threadpool.ThreadPool(3)
        requests_ = threadpool.makeRequests(get_index_page, [(item, None) for item in states.items()])
        [pool.putRequest(req) for req in requests_]
        pool.wait()
        time.sleep(60)

if not os.path.exists("./log"):
    os.makedirs("./log")
logging.basicConfig(level=logging.INFO,
                    filemode="a",
                    filename="./log/tjgb_update.log",
                    format='%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s', )
try:
    conn = MongoClientTools(url=CONFIG_MONGO['url'], db=CONFIG_MONGO['db'])
except Exception as e:
    logging.info('链接数据库Error--》%s' % e)


if __name__ == '__main__':
    main_update()