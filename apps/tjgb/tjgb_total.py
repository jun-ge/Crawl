#!/usr/bin/env python
# -*- coding: utf-8 -*-
#   @CreateTime    : 2018/11/5 16:15
#   @Author  : yanwj
#   @File    : tjgb_total.py

import logging
import os
import random
import re
import time
from datetime import datetime

import requests
from lxml import etree
from pyquery import PyQuery
import threadpool
from Tools.db_tools.mongo_tools import MongoClientTools
from Tools.http_tools import HEADERS, get_response
from config import CONFIG_MONGO

RESOURCE_NAME = 'tjgb'

def get_index_page(state, state_url):
    try:
        doc = PyQuery(get_response(state_url, headers=HEADERS).content.decode('gb2312', 'ignore'))
    except Exception as e:
        logging.info('{%s}页面解析错误--》%s' % (e))
    time.sleep(random.randint(1, 20) / 10)
    url_list = [li_tag('a').attr.href for li_tag in doc('.news_list  .box  li').items()]
    for url in url_list:
        if conn.search(CONFIG_MONGO['table'] + RESOURCE_NAME, {'链接': 'http://www.tjcn.org' + url}).count():
            logging.info('地址{%s}信息存在' % ('http://www.tjcn.org' + url))
            continue
        get_detail_page(state, 'http://www.tjcn.org' + url)
    if '下一页' in str(doc('.epages')):
        next_page = doc('.epages a').eq(-2).attr.href
        next_page_url = 'http://www.tjcn.org' + next_page
        get_index_page(state, next_page_url)


def get_detail_page(state, detail_url):
    try:
        doc = PyQuery(get_response(detail_url, headers=HEADERS).content.decode('gb2312', 'ignore'))
        time.sleep(random.randint(1, 20) / 10)
        title = doc('h1').text().strip()
        info = doc('.info_text').text().strip()
        if info:
            info_text = re.search(r'时间：(.*?)　来源：(.*?)　作者', info)
            pubdate = info_text.group(1)
            source = info_text.group(2)

    except Exception as e:
        logging.info('{%s}页面解析错误--》%s' % (detail_url, e))
        pubdate = ''
        source = ''
        title = ''
    source_url = detail_url
    # 获取 第一个数字的下标 ’普洱市宁洱县2011年国民经济和社会发展统计公报‘
    num_start_index = get_first_num_index(title)
    if not num_start_index:
        # 类似这种：
        # 中国七五时期国民经济和社会发展统计公报http://www.tjcn.org/tjgb/00zg/index_2.html
        year = ''
    else:
        year = title[num_start_index: num_start_index + 4]
        if year.startswith('0'):
            # 类似这种：xxx省015XXXX
            year = '2' + year[:-1]

    if title.startswith('中国'):
        city = ""
        state = ''
    else:
        city = title[:num_start_index]
    if state in city:
        city = ''
    if state in ['北京', '天津', '上海', '重庆']:
        state = '非省份，属于直辖市'
        city = title[:num_start_index]
    district = ""
    if '县' in city or '区' in city:
        city, district = city[:city.find('市') + 1], city[city.find('市') + 1:]

    content = ""
    content = get_content(detail_url, content)

    data = {
        '标题': title,
        '正文': content.replace('\r', ''),
        '发布时间': datetime.strptime(pubdate, '%Y-%m-%d %H:%M:%S') if pubdate != '' else '',
        '来源': source,
        '链接': source_url,
        '省份': state,
        '城市': city,
        '县/区': district,
        '年份': year,
        '抓取时间': datetime.now().strftime('%Y-%m-%d %H:%S:%M')
    }
    logging.info('正在存储数据--->%s:%s' % (title, source_url))
    conn.save(data, CONFIG_MONGO['table'] + RESOURCE_NAME)
    # print(data)


def get_content(url, content):
    response = get_response(url, headers=HEADERS)
    time.sleep(random.randint(1, 10) / 10)
    html = response.content.decode('gb2312', 'ignore')
    doc = PyQuery(html)
    select = etree.HTML(html)
    content += doc('#text').remove('.pageLink').text()
    if select.xpath('//p[@class="pageLink"]//a[contains(text(), "下一页")]'):
        next_page_url = 'http://www.tjcn.org' + \
                        select.xpath('//p[@class="pageLink"]//a[contains(text(), "下一页")]/@href')[0]
        content = get_content(next_page_url, content)
    return content


def get_first_num_index(s):
    for c in range(len(s)):
        if 48 <= ord(s[c]) <= 57:
            return c
    return False


def main_total():
    url = 'http://www.tjcn.org/tjgb/'
    doc = PyQuery(requests.get(url).content)
    states = {}
    a_tags = doc('.zlm a')
    for a in a_tags.items():
        states[a.text()] = 'http://www.tjcn.org' + a.attr.href
    logging.info(states)
    pool = threadpool.ThreadPool(10)
    # 多个参数，多线程
    requests_ = threadpool.makeRequests(get_index_page, [(item, None) for item in states.items()])
    [pool.putRequest(req) for req in requests_]
    pool.wait()

if not os.path.exists("./log"):
    os.makedirs("./log")
logging.basicConfig(level=logging.INFO,
                    filemode="a",
                    filename="./log/tjgb_total.log",
                    format='%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s', )
try:
    conn = MongoClientTools(url=CONFIG_MONGO['url'], db=CONFIG_MONGO['db'])
except Exception as e:
    logging.info('链接数据库Error--》%s' % e)


if __name__ == '__main__':
    main_total()