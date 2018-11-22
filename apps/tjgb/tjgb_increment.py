#!/usr/bin/env python
# -*- coding: utf-8 -*-
#   @CreateTime    : 2018/11/5 16:15
#   @Author  : yanwj
#   @File    : tjgb_pro.py

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

# 获取列表页面的详情url
from config import CONFIG_MONGO

RESOURCE_NAME = 'tjgb'


def get_index_page(state, state_url):
    count = 0
    doc = PyQuery(get_response(state_url, headers=HEADERS).content)
    time.sleep(random.randint(1, 20) / 10)
    url_list = [li_tag('a').attr.href for li_tag in doc('.news_list  .box  li').items()]
    for url in url_list:
        # 判断单个省份第一页的详情页的url，如果存在数据库中则不再爬取
        if conn.search(CONFIG_MONGO['table'] + RESOURCE_NAME, {'链接': 'http://www.tjcn.org' + url}).count():
            continue
        get_detail_page(state, 'http://www.tjcn.org' + url)
        count += 1
    logging.info('%s 数据查询完毕，更新数据  %s条' % (state, count))


# 获取详情页信息
def get_detail_page(state, detail_url):
    doc = PyQuery(get_response(detail_url, headers=HEADERS).content)
    title = doc('h1').text().strip()
    info_text = re.search(r'时间：(.*?)　来源：(.*?)　作者', doc('.info_text').text().strip())
    pubdate = info_text.group(1)
    source = info_text.group(2)
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
        # 若是没有 '市' find返回-1，city为空
        city, district = city[:city.find('市') + 1], city[city.find('市') + 1:]

    content = ""
    content = get_content(detail_url, content)

    data = {
        '标题': title,
        '正文': content.replace('\r', ''),
        '发布时间': datetime.strptime(pubdate, '%Y-%m-%d %H:%M:%S'),
        '来源': source,
        '链接': source_url,
        '省份': state,
        '城市': city,
        '县/区': district,
        '年份': year,
        '抓取时间': datetime.now().strftime('%Y-%m-%d %H:%S:%M')
    }
    logging.info('正在存储新增数据--->{%s}{%s}{%s}:%s' % (pubdate, state, title, source_url))
    conn.save(data, CONFIG_MONGO['table'] + RESOURCE_NAME)


# 获取文章内容
def get_content(url, content):
    response = get_response(url, headers=HEADERS)
    time.sleep(0.1)
    html = response.content.decode('gb2312', 'ignore')
    doc = PyQuery(html)
    select = etree.HTML(html)
    content += doc('#text').remove('.pageLink').text()
    # pyquery 无法正常获取pagelink对应的p标签，暂用xpath写，后期抗情况改掉
    if select.xpath('//p[@class="pageLink"]//a[contains(text(), "下一页")]'):
        next_page_url = 'http://www.tjcn.org' + \
                        select.xpath('//p[@class="pageLink"]//a[contains(text(), "下一页")]/@href')[0]
        content = get_content(next_page_url, content)
    return content


def get_first_num_index(s):
    """
    返回字符串中第一个数字的下标
    :param s:
    :return:
    """
    for c in range(len(s)):
        if 48 <= ord(s[c]) <= 57:
            return c
    return False


def main_increment():
    while True:
        url = 'http://www.tjcn.org/tjgb/'
        doc = PyQuery(requests.get(url).content)
        states = {}
        a_tags = doc('.zlm a')
        for a in a_tags.items():
            states[a.text()] = 'http://www.tjcn.org' + a.attr.href
        logging.info(states)
        pool = threadpool.ThreadPool(10)
        requests_ = threadpool.makeRequests(get_index_page, [(item, None) for item in states.items()])
        [pool.putRequest(req) for req in requests_]
        pool.wait()
        time.sleep(24 * 60 * 60)


if not os.path.exists("./log"):
    os.makedirs("./log")
logging.basicConfig(level=logging.INFO,
                    filemode="a",
                    filename="./log/tjgb_inc.log",
                    format='%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s', )
try:
    conn = MongoClientTools(url=CONFIG_MONGO['url'], db=CONFIG_MONGO['db'])
    # conn = MongoClientTools(url='mongodb://localhost:27017', db=u'YWJ(TEST)')
except Exception as e:
    logging.info('链接数据库Error--》%s' % e)




if __name__ == '__main__':
    main_increment()
