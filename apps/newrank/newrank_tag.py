#!/usr/bin/env python
# -*- coding: utf-8 -*-
#   @CreateTime    : 2018/11/13 14:02
#   @Author  : yanwj
#   @File    : newrank_tag.py
import json
import logging
import os
import random
import re
import time
from datetime import datetime

import js2py
import threadpool
from pyquery import PyQuery

from Tools.db_tools.mongo_tools import MongoClientTools
from Tools.http_tools import get_response
from apps.newrank.newrank_rank import GetNewrankJS
from config import CONFIG_MONGO


SOURCE = "Tag"
PARSER_MODULES = {
    # 登入解析模板
    'username_login': '/xdnphb/login/new/usernameLogin?AppKey=joker&flag={0}&identifyCode=&password={2}&username={1}&nonce=',
    # 单个公众号解析模板
    'weixindata_one': '/xdnphb/data/weixinuser/searchWeixinDataByCondition?AppKey=joker&filter=&hasDeal=false&keyName={0}&order=relation&nonce=',
    # 按类别的公众号解析模板
    'weixindata_many': '/xdnphb/data/weixinuser/searchWeixinDataByCondition?AppKey=joker&filter=tags&hasDeal=false&keyName={0}&order=NRI&nonce=',
    # 微信号info 详细页面tag标签获取解析模板
    'info_tag': '/xdnphb/twomicroandtag/tag/getTagByAccountId?AppKey=joker&account_id={}&nonce=',
    # getTagByAccountId,值,为uuid
}

USERS = [{'username': '13072761557', 'password': '2623647c9d99f7959c64330b12a4a91a'},
         {'username': '15262595457', 'password': '1f65a5475059bf0b6584198df44b6ece'},
         {'username': '18529072372', 'password': '6059ef018901adde2c239ab3bda39387'},
         {'username': '15527183105', 'password': '24e9bb22f0f88e073d3d710c73d30b34'},
         {'username': '15619255619', 'password': '6059ef018901adde2c239ab3bda39387'},
         {'username': '18122041556', 'password': 'de2b9a7b715f28258e1024c3abe5229e'},
         {'username': '13296621557', 'password': '70f057a41a8d6378952e5604f87f7b24'},
         {'username': '18576477847', 'password': '1f65a5475059bf0b6584198df44b6ece'},
         {'username': '13049487876', 'password': '962c06c74df33cb7ce4e4361e6e2a1f0'},
         {'username': '15872371734', 'password': 'e6908815aad7ba628e0625e5d9b144d8'},
         {'username': '15971440699', 'password': 'e6908815aad7ba628e0625e5d9b144d8'},
         {'username': '18571621267', 'password': 'e6908815aad7ba628e0625e5d9b144d8'},
         {'username': '17612720192', 'password': 'e6908815aad7ba628e0625e5d9b144d8'},
         {'username': '18571869616', 'password': 'e6908815aad7ba628e0625e5d9b144d8'},
         ]

TAGS = ['财富', '商业', '财经', '金融业', '股市', '金融', 'IPO', '互联网', '创业', '管理', '楼市', '房产', '银行', '互联金融', '消费金融', '信用卡', '资产管理',
        'P2P', '科技', '保险', '理财', '证券', '基金', '并购重组', '新三板', '私募', '外汇', '期货', '智能投资', ]


class NewrankTag:
    def __init__(self):
        self.request_times = [1]
        self.url = 'https://www.newrank.cn'
        self.tag_info_url = 'https://www.newrank.cn/public/info/detail.html?account='
        self.conn = MongoClientTools(url=CONFIG_MONGO['url'], db=CONFIG_MONGO['db2'])
        self.table = CONFIG_MONGO['table2'] + SOURCE
        self.get_js_result = GetNewrankJS()
        self.accounts_from_rank = self.get_account_from_rank()
        self.response_queue = []
        user = random.choice(USERS)
        self.token = self.get_token(user['username'], user['password'])

    def get_account_from_rank(self):
        """
        根据榜单获取公众号的account，去重
        :return:
        """
        accounts = set()
        data = self.conn.search('WeChat_OffiAccot_Rank', '详情')
        for item in data:
            for account in item['datas']:
                accounts.add(account['account'].lower())
        return accounts

    def get_parse_url(self, module):
        """
        获取添加参数的后的url
        :param module:
        :return:
        """
        parse_result = self.get_js_result.run(module)
        url = self.url + module.replace('AppKey=joker&', '') + parse_result[
            'nonce'] + '&xyz=' + parse_result['xyz']
        return url

    def get_token(self, username, password):
        '''
        获取token值
        :return:
        '''
        flag = js2py.eval_js('''
            x = function(){
            var codeFlag = (new Date).getTime()+ "" + Math.random();
            return codeFlag
            };
            x();
             ''')

        while True:
            module = PARSER_MODULES['username_login'].format(flag, username, password)
            try:
                url = self.get_parse_url(module)
                res = get_response(url)
                enter_msg = res.json()
                if enter_msg['value'].get('msg', None) == "登录成功":
                    return enter_msg['value']['token']
                else:
                    logging.info('%s，code :-3{%s}, ' % (enter_msg['value'].get('msg', None), module))
                    user = random.choice(USERS)
                    username = user['username']
                    password = user['password']
                    continue
            except Exception as e:
                logging.info('登入新榜出错,跟换用户->错误信息{%s},{%s} ' % (module, e))
                user = random.choice(USERS)
                username = user['username']
                password = user['password']

    def get_tagMsg_from_tags(self):
        """
        根据tag分类标签，批量获取tag相关信息，每个分类只有50条数据
        :return:
        """
        for tag in TAGS:
            module = PARSER_MODULES['weixindata_many'].format(tag)
            url = self.get_parse_url(module)
            res = self.get_tag_response(url)
            base_info = res.json()['value']
            # 对榜单里的account去重
            for item in base_info['result']:
                if item['account'] in self.accounts_from_rank:
                    self.accounts_from_rank.remove(item['account'])
                elif item['accountLower'] in self.accounts_from_rank:
                    self.accounts_from_rank.remove(item['accountLower'])
            yield {'tag分类': tag, '基本信息': base_info, '抓取时间': datetime.now()}

    def get_tagMsg_from_account(self):
        """
        根据单个account获取单个tag的相关信息.
        :return:
        """

        total = len(self.accounts_from_rank)
        accounts_info = {}
        for account in self.accounts_from_rank:
            module = PARSER_MODULES['weixindata_one'].format(account)
            url = self.get_parse_url(module)
            res = self.get_tag_response(url)
            base_info = res.json()['vaule']
            accounts_info.update({account: base_info})
        return {'tag分类': '其它', '总微信号数': total, '基本信息': accounts_info}

    def get_tag_response(self, url):
        '''
        发送请求，返回response
        :param url:
        :return:
        '''
        while True:
            try:
                response = get_response(url, cookies={'token': self.token})
                #time.sleep(random.randint(1, 20) / 10)
                self.request_times.append(1)
                if len(self.request_times) %100  == 0:
                    user = random.choice(USERS)
                    self.token = self.get_token(user['username'], user['password'])
                    logging.info('切换用户（%s）登入' % user['username'])
                try:
                    if response.json()['value']:
                        # 这里处理，获取的json数据，非json数据走下面流程
                        return response
                    elif response.json():
                        # 这里处理，获取的json数据，非json数据走下面流程
                        return response
                    else:
                        user = random.choice(USERS)
                        self.token = self.get_token(user['username'], user['password'])
                        logging.info('切换用户（%s）登入' % user['username'])
                except Exception as e:
                    title = PyQuery(response.content.decode('utf-8'))('title').text()
                    if title in ['新榜——欢迎登录', '页面错误', '异常']:
                        time.sleep(random.randint(1, 5))
                        user = random.choice(USERS)
                        self.token = self.get_token(user['username'], user['password'])
                        logging.info('token 失效,切换新用户{ %s}' % user['username'])
                        continue
                    # 非json数据页面，直接返回
                    else:
                        return response
            except Exception as e:
                logging.info("{%s}{%s}" % (url, e))

    def parse_tag_info_page(self, response):
        """
        使用pyquery解析详情页面
        :param response:
        :return:
        """
        html = response.content.decode('utf-8', 'ignore')
        doc = PyQuery(html)
        # 最近7天的新榜指数信息
        try:
            esbclf = re.search('var esbclf = (.*?)lastUpdateTime":".*?}', html).group().replace('var esbclf =',
                                                                                                '').strip()
            # 基本信息dict格式
            fgkcdg = re.search('var fgkcdg = (.*?)}', html).group().replace('var fgkcdg =', '').strip()
            fgkcdg = json.loads(fgkcdg.replace('\'', '\"'))
            account_id = fgkcdg.get('uuid', None)
        except Exception as e:
            logging.info('response{url:%s}正则匹配失败errr: %s' % (response.url, e))
            fgkcdg = esbclf = ''
            try:
                account_id = re.search('uuid=(.*?)"', html).group(1)
            except:
                account_id = None
        module = PARSER_MODULES['info_tag'].format(account_id)
        url = self.get_parse_url(module)
        res = self.get_tag_response(url)
        tags = '|'.join([item['name'] for item in res.json()['value']])
        if fgkcdg != "":
            fgkcdg.update({
                "fans-counts": doc('.detail-fans-counts').text().strip(),
                'tags': tags
            })

        return {
            'info': fgkcdg,
            'data': json.loads(esbclf) if esbclf else None,
            'create_time': datetime.now(),
        }

    def save_tag(self):
        """
        从榜单和分类标签获两处取所有的微信号简介，不重复
        :return:
        """
        for data in self.get_tagMsg_from_tags():
            self.conn.save(data, self.table)
            logging.info('正在保存{%s} 的数据' % data['tag分类'])
            # return
        # time.sleep(10)
        # 榜单里面微信号简介，是否单独爬取待定
        # self.conn.save(self.get_account_from_rank(), self.table)

    def save_tag_info(self, request, result):
        """
        保存微信号的详细信息
        :param request:
        :param result:
        :return:
        """
        # 获取info页面解析后的数
        data = self.parse_tag_info_page(result)
        # 添加一个目标url
        data.update({'source_url': request.args[0], 'wx_account': request.args[0].split('=')[-1]})
        self.conn.save(data, CONFIG_MONGO['table2'] + 'Info')
        logging.info('成功存储微信号的info{%s}' % request.args[0])

    def run_tag_info(self):

        data = self.conn.search('WeChat_OffiAccot_Tag', '基本信息')
        data_exist = list(self.conn.search('WeChat_OffiAccot_Info', 'wx_account'))
        account = set()
        for d in data:
            data2 = d['result']
            for item2 in data2:
                account.add(item2['accountLower'])
        all_account = list(set((self.accounts_from_rank) | account) - set(data_exist))
        logging.info('总计微信号%s， 已下载%s个' % (len(self.accounts_from_rank | account), len(data_exist)))

        all_parse_urls = [self.tag_info_url + account for account in all_account]
        # 开启多线程处理，请求并解析页面
        pool = threadpool.ThreadPool(1)
        request_queue = threadpool.makeRequests(self.get_tag_response, all_parse_urls, callback=self.save_tag_info)
        [pool.putRequest(req) for req in request_queue]
        pool.wait()

    def run_tags(self):
        self.save_tag()


if __name__ == '__main__':
    if not os.path.exists('./log'):
        os.mkdir('./log')
    logging.basicConfig(level=logging.INFO,
                        filemode="a",
                        filename="./log/newrank_info.log",
                        format='%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s', )
    newrank = NewrankTag()
    # newrank.run_tags()
    newrank.run_tag_info()
