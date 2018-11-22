#!/usr/bin/env python
# -*- coding: utf-8 -*-
#   @CreateTime    : 2018/11/22 11:19
#   @Author  : yanwj
#   @File    : qcc_test.py
import logging
import os
import time
from pyquery import PyQuery

from Tools.db_tools.redis_tools import RedisConnection
from Tools.http_tools import get_response, get_proxy
from config import CONFIG_REDIS

redis_conn = RedisConnection().redis_connect(**CONFIG_REDIS)


def save_company_url(response, company_name):
    doc = PyQuery(response.content)
    title = doc('title').text()
    if title in ['会员登录 - 企查查']:
        logging.info('需要登录')
        return
    elif title in ['用户验证_企查查']:
        logging.info('需要处理验证码')
        return
    elif company_name not in title:
        logging.info('页面错误')
        return
    a = doc('.m_srchList tbody tr').eq(0)('td').eq(1)('a')
    company_url = 'https://www.qichacha.com' + a.attr.href
    redis_conn.hset('qcc_company_urls', company_name, company_url)
    return True

def save_company_url_sj(response, company_name):
    doc = PyQuery(response.content)
    title = doc('title').text()

    if title in ['会员登录 - 企查查']:
        logging.info('需要登录')
        return
    elif title in ['用户验证_企查查']:
        logging.info('需要处理验证码')
        return
    elif company_name not in title:
        logging.info('页面错误')
        return

    company_url = 'https://m.qichacha.com' + doc('.list-wrap a').eq(0).attr.href
    redis_conn.hset('qcc_company_urls', company_name, company_url)
    return True

def run(url):

    while True:
        company_name = redis_conn.spop('qcc_company_name').decode('utf-8', 'ignore')
        if redis_conn.hexists('qcc_company_urls', company_name):
            continue
        params = {'key': company_name}
        cookie = get_cookie('https://m.qichacha.com')
        print(cookie.items())
        try:
            response = get_response(url, params=params, cookies=cookie)
            if url == 'https://m.qichacha.com/search':
                result = save_company_url_sj(response, company_name)
            else:
                result = save_company_url(response, company_name)
            if not result:
                redis_conn.sadd('qcc_company_name', company_name)
            time.sleep(3)
        except Exception as e:
            redis_conn.sadd('qcc_company_name', company_name)
            logging.info(e)


def get_cookie(url):
    response = get_response(url)
    return response.cookies


if __name__ == '__main__':
    #
    # with open('companys.txt', 'r', encoding='utf-8') as fr:
    #     companys = [com.strip() for com in fr.readlines()]
    # redis_conn.sadd('qcc_company_name',*companys)
    # #
    if not os.path.exists('./log'):
        os.mkdir('./log')

    logging.basicConfig(level=logging.INFO,
                        filemode="a",
                        filename="./log/qcc_info.log",
                        # encoding='utf-8',
                        format='%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s', )
    url = 'https://www.qichacha.com/search'
    url_sj = 'https://m.qichacha.com/search'
    run(url)
