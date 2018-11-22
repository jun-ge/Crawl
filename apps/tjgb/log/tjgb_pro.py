#!/usr/bin/env python
# -*- coding: utf-8 -*-
#   @CreateTime    : 2018/11/5 16:15
#   @Author  : yanwj
#   @File    : tjgb_pro.py

import logging
import os
import re
import time
from datetime import datetime
import requests
from lxml import etree
from pyquery import PyQuery
from Tools.db_tools.mongo_tools import MongoClientTools


def get_index_page(state, state_url):
    doc = PyQuery(requests.get(state_url).content)
    url_list = [li_tag('a').attr.href for li_tag in doc('.news_list  .box  li').items()]
    for url in url_list:
        get_detail_page('http://www.tjcn.org' + url, state)
    if '下一页' in str(doc('.epages')):
        next_page = doc('.epages a').eq(-2).attr.href
        next_page_url = 'http://www.tjcn.org' + next_page
        get_index_page(state, next_page_url)
        time.sleep(0.1)


def get_detail_page(detail_url, state):
    # if getattr(conn, '统计公报').find({'链接': detail_url}).count():
    #   return
    doc = PyQuery(requests.get(detail_url).content)
    title = doc('h1').text().strip()
    info_text = re.search(r'时间：(.*?)　来源：(.*?)　作者', doc('.info_text').text().strip())
    pubdate = info_text.group(1)
    source = info_text.group(2)
    source_url = detail_url
    # 获取 第一个数字的下标 ’普洱市宁洱县2011年国民经济和社会发展统计公报‘
    num_start_index = get_first_num_index(title)
    if not num_start_index:
        # 中国七五时期国民经济和社会发展统计公报http://www.tjcn.org/tjgb/00zg/index_2.html
        year = title[2:6]
    else:
        year = title[num_start_index: num_start_index + 4]
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
    content = doc('#text').remove('.pageLink').text()
    html = etree.HTML(requests.get(detail_url).content)
    # 翻页
    while html.xpath('//td[@id="text"]//p[@class="pageLink"]/a[text()="下一页"]/@href'):
        next_content_url = 'http://www.tjcn.org' + html.xpath('//p[@class="pageLink"]/a[text()="下一页"]/@href')[0]
        html = etree.HTML(requests.get(next_content_url).content)
        content_element = html.xpath('//td[@id="text"]')[0]
        try:
            content_last_element = content_element.xpath('./*[last()]')[0]
            pageLink_element = html.xpath('//p[@class="pageLink"]')[0]
            # 移除翻页标签p，先删除最后一个元素，若最后一个为<div>xxxx<p></p></div>形式则，先删除p,再添加div
            content_element.remove(content_last_element)
            if content_last_element != pageLink_element:
                content_last_element.remove(pageLink_element)
                content_element.append(content_last_element)
        except Exception as e:
            logging.info('错误链接%s, %s' % (next_content_url, e))
            time.sleep(1)

        # //text()获取所有子孙节点文本
        content += ''.join(content_element.xpath('//td[@id="text"]//text()'))
        html = etree.HTML(requests.get(next_content_url).content)

    data = {
        '标题': title,
        '正文': content.replace('\r', ''),
        '发布时间': pubdate,
        '来源': source,
        '链接': source_url,
        '省份': state,
        '城市(地区)': city,
        '年份': year,
        '抓取时间': datetime.now().strftime('%Y-%m-%d %H:%S:%M')
    }
    logging.info(data)
    conn.save(data, table_name='统计公报')


def get_first_num_index(s):
    for c in range(len(s)):
        if 48 <= ord(s[c]) <= 57:
            return c
    return False


if __name__ == '__main__':

    if not os.path.exists("./log"):
        os.makedirs("./log")
    logging.basicConfig(level=logging.INFO,
                        filemode="a",
                        filename="./log/tjgb.log",
                        format='%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s', )
    try:
        conn = MongoClientTools(url='mongodb://172.18.83.123:27018', db=u'统计公报(TEST)')
        # conn = MongoClientTools(url='mongodb://localhost:27017', db=u'统计公报(TEST)')
    except Exception as e:
        logging.info('链接数据库Error--》%s' % e)

    url = 'http://www.tjcn.org/tjgb/'
    doc = PyQuery(requests.get(url).content)
    states = {}
    a_tags = doc('.zlm a')
    for a in a_tags.items():
        states[a.text()] = 'http://www.tjcn.org' + a.attr.href
    logging.info(states)

    for state, state_url in states.items():
        get_index_page(state, state_url)
