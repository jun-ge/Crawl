#!/usr/bin/env python
# -*- coding: utf-8 -*-
#   @CreateTime    : 2018/11/8 16:08
#   @Author  : yanwj
#   @File    : newrank_rank.py

# https://www.newrank.cn/public/info/list.html?period=day&type=data正常访问网站
# https://www.newrank.cn/xdnphb/list/day/rank?post请求
# https://www.newrank.cn/xdnphb/list/week/rank？post请求
# https://www.newrank.cn/xdnphb/list/month/rank？post请求
import json
import logging
import os
import threading
import time
from datetime import datetime, timedelta
import threadpool
import js2py
from Tools.db_tools.mongo_tools import MongoClientTools
from Tools.db_tools.redis_tools import RedisConnection
from Tools.http_tools import get_response
from config import CONFIG_MONGO, CONFIG_REDIS

SOURCE = 'Rank'
# 日榜，周榜，月榜
LIST_TYPE = ['day', 'week', 'month']
# 模块
MODULES = ['时事', '民生', '财富', '科技', '创业', '汽车', '楼市', '职场', '教育', '学术', '政务', '企业',
           '文化', '百科', '健康', '时尚', '美食', '乐活', '旅行', '幽默', '情感', '体娱', '美体', '文摘']

RANK_NAME_GROUP = '资讯'

formdata = {
    'end': '2018-10-31',
    'rank_name': '时事',
    'rank_name_group': '资讯',
    'start': '2018-10-01',
    'nonce': '9e832ba06',
    'xyz': '84f3af804b2f9a101dbe8e19d2d2f1ff',
}
#  xyz 参数加密需要模板种类
XYZ_PARSER_MODULES = {
    'getFull': '',
    'getAdvertBannerImage': '',
    'getDate': '',
    'getSampleRecord': "/xdnphb/list/getSampleRecord?AppKey=joker&date={0}&nonce=",
    'rank': "/xdnphb/list/{0}/rank?AppKey=joker&end={2}&rank_name={3}&rank_name_group={4}&start={1}&nonce=",
}


class GetNewrankJS:
    def __init__(self):
        with open('newrank_js_code.js', 'r', encoding='gb18030') as fr:
            self.js_code = fr.read()

        # .format('day', formdata['end'], formdata['rank_name'], formdata['rank_name_group'], formdata['start'])

    # 执行js文件获取nonce和xyz
    def run(self, parser_module):
        while True:
            try:
                return js2py.eval_js(self.js_code.replace('666666', parser_module))
            except Exception as e:
                logging.info(parser_module + '加密错误', e)
                time.sleep(60)


class NewRank:
    def __init__(self):
        self.redis_conn = RedisConnection().redis_connect(**CONFIG_REDIS)
        self.conn = MongoClientTools()
        self.hours = datetime.now().hour
        self.day = datetime.now().day
        self.week = datetime.now().weekday()
        self.year = datetime.now().year
        self.month = datetime.now().month
        self.get_js_result = GetNewrankJS()
        # 待加密的队列
        self.parser_module_queue = []
        self.get_all_parser_module()
        # url队列
        self.request_queue = []
        # self.get_request_queue()  # 单线程处理加密队列
        self.thread_get_parser_url()  # 多线程处理加密队列

    def get_history_date(self):
        """
        根据榜单获取统计时间区间，去重
        :return:
        """
        date_range = set()
        dates = self.conn.search('WeChat_OffiAccot_Rank')
        for item in dates:
            date_range.add(item['统计时间区间'])
        return date_range

    def get_all_parser_module(self):
        start_date = datetime(self.year, self.month, self.day)
        # 如果当前的小时早于中午12点，则最近一天显示的是前天的统计信息，反之是统计的昨天的信息
        # 日榜情况：最近7天的数据可以查询到，前一天数据需要第二天12点截止才能获取到
        if self.hours > 12:
            history_days = [(start_date - timedelta(1 + n)).strftime('%Y-%m-%d') for n in range(7)]
        else:
            history_days = [(start_date - timedelta(2 + n)).strftime('%Y-%m-%d') for n in range(7)]

        for day in history_days:
            time_range_day = '(%s, %s)' % (day, day)
            if self.redis_conn.sismember('newrank_time_range_filter', time_range_day):
                continue
            self.redis_conn.sadd('newrank_time_range_filter', time_range_day)
            sample_size = self.get_samplesize(day)
            # 每天，的24个种类模块
            self.parser_module_queue.extend(
                [{'module': XYZ_PARSER_MODULES['rank'].format('day', day, day, rank_name, '资讯'),
                  'list_type': '日榜',
                  'rank_name': rank_name,
                  'rank_name_group': '资讯',
                  'start_date': day,
                  'end_date': day,
                  'samplesize': sample_size,
                  } for rank_name in MODULES])

        # 周榜情况：本次周期10.29-11.04。数据星期一12点后截止统计
        # 获取最近一周的起始日期
        week_start_lately = start_date - timedelta(self.week)
        week_end_lately = week_start_lately + timedelta(6)
        # 星期一为0，星期天为6
        #  如果不为星期一，获取上周的周起始时间结束时间
        if self.week > 0:
            # 根据最近的星期周期，获取更早两周的周期,统计近三周的数据
            history_weeks = [((week_start_lately - timedelta(n * 7)).strftime('%Y-%m-%d'),
                              (week_end_lately - timedelta(n * 7)).strftime('%Y-%m-%d')) for n in range(1, 4)]
        else:
            # 如果为星期一,判断时间是否在12点之前，在12点之前的，则只能获取的上上周的数据
            if self.hours > 12:
                # 最近一周为上周
                history_weeks = [((week_start_lately - timedelta(n * 7)).strftime('%Y-%m-%d'),
                                  (week_end_lately - timedelta(n * 7)).strftime('%Y-%m-%d')) for n in range(1, 4)]
            else:
                # 最近的一周为上上周
                history_weeks = [((week_start_lately - timedelta(n * 7)).strftime('%Y-%m-%d'),
                                  (week_end_lately - timedelta(n * 7)).strftime('%Y-%m-%d')) for n in range(2, 5)]
        for week in history_weeks:
            time_range_week = '(%s, %s)' % (week[0], week[1])
            if self.redis_conn.sismember('newrank_time_range_filter', time_range_week):
                continue
            self.redis_conn.sadd('newrank_time_range_filter', time_range_week)
            sample_size = self.get_samplesize(week[1])
            # 每周24个种类的解析模板
            self.parser_module_queue.extend(
                [{'module': XYZ_PARSER_MODULES['rank'].format('week', week[0], week[1], rank_name, '资讯'),
                  'list_type': '周榜',
                  'rank_name': rank_name,
                  'rank_name_group': '资讯',
                  'start_date': week[0],
                  'end_date': week[1],
                  'samplesize': sample_size,
                  } for rank_name in MODULES])

        # 月榜每月一次，一般在1号12点以后，只能获取最近三月的情况
        # 获取当前月份，若当前时间大于当前月的1号的12点,则最近月为上一个月，否则为上上个月
        if datetime(self.year, self.month, self.day, self.hours) > datetime(self.year, self.month, 1, 12):
            # 获取最近三月的第一天和最后一天
            histtory_months = [(datetime(self.year, self.month - n, 1).strftime('%Y-%m-%d'),
                                (datetime(self.year, self.month - (n - 1), 1) - timedelta(1)).strftime('%Y-%m-%d'))
                               for n in range(1, 4)]
        else:
            histtory_months = [(datetime(self.year, self.month - n, 1).strftime('%Y-%m-%d'),
                                (datetime(self.year, self.month - (n - 1), 1) - timedelta(1)).strftime('%Y-%m-%d'))
                               for n in range(2, 5)]
        for month in histtory_months:
            time_range_month = '(%s, %s)' % (month[0], month[1])
            if self.redis_conn.sismember('newrank_time_range_filter', time_range_month):
                continue
            self.redis_conn.sadd('newrank_time_range_filter', time_range_month)
            sample_size = self.get_samplesize(month[1])
            # 每y月24个种类的解析模板
            self.parser_module_queue.extend(
                [{'module': XYZ_PARSER_MODULES['rank'].format('month', month[0], month[1], rank_name, '资讯'),
                  'list_type': '月榜',
                  'rank_name': rank_name,
                  'rank_name_group': '资讯',
                  'start_date': month[0],
                  'end_date': month[1],
                  'samplesize': sample_size,
                  } for rank_name in MODULES])

        return self.parser_module_queue

    def get_samplesize(self, date):
        """
        获取样板数量,
        :return:str样板数量值
        """
        parser_module = XYZ_PARSER_MODULES['getSampleRecord'].format(date)
        # 获取加密结果
        result = self.get_js_result.run(parser_module)
        url = 'https://www.newrank.cn' + parser_module.replace('AppKey=joker&', '') + result['nonce'] + '&xyz=' + \
              result['xyz']
        while True:
            response = get_response(url)
            try:
                sanmplsize = response.json()['value']
                if sanmplsize:
                    return sanmplsize
            except Exception as e:
                logging.info('获取json数据错误--》%s' % e)
                # print('获取json数据错误--》%s\n%s' % (e, response.json()))
            time.sleep(10)

    def get_request_queue(self):
        pass
        # # 单线程js加密算法处理特别慢,但是js2py处理加密不会报错
        # for parse_module in self.parser_module_queue:
        #     logging.info(' 板块：{%s}, 类别：{%s} 起始时间(%s, %s) 正在解密参数......' % (
        #         parse_module['list_type'], parse_module['rank_name'], parse_module['start_date'],
        #         parse_module['end_date']))
        #     # 获取加密结果
        #     result = self.get_js_result.run(parse_module['module'])
        #     parse_module['url'] = 'https://www.newrank.cn' + parse_module['module'].replace('AppKey=joker&', '') + \
        #                           result['nonce'] + '&xyz=' + result['xyz']
        #     logging.info('成功获取解密后的POST链接:{%s}' % parse_module['url'])
        #     self.request_queue.append(parse_module)
        #     break
        #
        # logging.info('全部解密完成，共计url %s 条' % len(self.request_queue))
        # return self.request_queue

    def thread_get_parser_url(self):
        """
        线程池:利用15个线程进行解密处理(总计需要获取日榜7 * 24 + 周榜3*24 + 月榜3*24 = 312 条url)
        :return:
        """
        modules = [item['module'] for item in self.parser_module_queue]
        pool = threadpool.ThreadPool(30)
        parser_queue = threadpool.makeRequests(self.get_js_result.run, modules, callback=self.callback)
        [pool.putRequest(url) for url in parser_queue]
        pool.wait()

    def callback(self, request, result):
        """
        线程池的回调函数
        :param request:<WorkRequest id=161684720 args=[函数参数] kwargs={} exception=False>可以通过request.arg[0]获取执行函数的参数
        :param result:执行函数的返回值
        :return:
        """
        url = 'https://www.newrank.cn' + request.args[0].replace('AppKey=joker&', '') + result['nonce'] + '&xyz=' + \
              result['xyz']
        logging.info('成功获取解密后的POST链接:{%s}' % url)
        for item in self.parser_module_queue:
            # 将新生成的链接存入parser_module_queue里对应的每个元素
            if request.args[0] == item['module']:
                item['url'] = url
                self.redis_conn.lpush('newrank_request', item)
                # self.request_queue.append(item)

    def get_and_save_json(self):
        """
        从redis队列，拿到url数据，请求并将结果存到mongo
        :return:
        """
        while True:
            item = self.redis_conn.spop('newrank_request_item')
            if not item:
                break
            item = eval(item)
            while True:
                response = get_response(item['url'])
                try:
                    detail = response.json()
                    if detail:
                        detail = detail['value']
                        detail.update({'samplesize': item['samplesize']})
                        break
                except Exception as e:
                    logging.info('获取json数据错误--》%s' % e)
                time.sleep(10)
            result = {
                '抓取时间': datetime.now().strftime('%Y-%m-%d %H:%S:%M'),
                '统计时间区间': '(%s, %s)' % (item['start_date'], item['end_date']),
                '统计截止日期': datetime.strptime(item['end_date'], '%Y-%m-%d') + timedelta(days=1, hours=12),
                '榜单类型': item['list_type'],
                '模块': item['rank_name'],
                '详情': detail
            }
            logging.info('正在存入数据 {%s: %s %s} {}' % (result['榜单类型'], result['模块'], result['统计时间区间']))
            self.conn.save(result, CONFIG_MONGO['table2'] + SOURCE)

    def run(self):
        for i in range(3):
            th = threading.Thread(target=self.get_and_save_json)
            th.start()


if __name__ == '__main__':
    if not os.path.exists('./log'):
        os.mkdir('./log')
    logging.basicConfig(level=logging.INFO,
                        filemode="a",
                        filename="./log/newrank_rank.log",
                        format='%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s', )
    newrank = NewRank()
    newrank.run()

