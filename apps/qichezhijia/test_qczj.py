#!/usr/bin/env python
# -*- coding: utf-8 -*-
#   @CreateTime    : 2018/11/21 10:49
#   @Author  : yanwj
#   @File    : test_qczj.py


# url = 'https://www.autohome.com.cn/beijing/'
import re

import requests
from pyquery import PyQuery

from Tools.db_tools.mongo_tools import MongoClientTools
from Tools.db_tools.redis_tools import RedisConnection
from Tools.http_tools import get_response
from config import CONFIG_REDIS, CONFIG_MONGO

car_rank = {
    'a00': '微型车',
    'a0': '小型车',
    'a': '紧凑型车',
    'b': '中型车',
    'c': '中大型车',
    'd': '大型车',
    'suv': 'SUV',
    'mpv': 'MPV',
    's': '跑车',
    'p': '皮卡',
    'mb': '微面',
    'qk': '轻客',
}

key = 'a00'
url = 'https://www.autohome.com.cn/{}/'.format(key)

res = requests.get(url)

# print(res.text)
mongo_conn = MongoClientTools(**CONFIG_MONGO)
redis_conn = RedisConnection().redis_connect(**CONFIG_REDIS)

city_items = re.search('<script language="javascript" type="text/javascript">var CityItems = (.*?);</script>',
                       res.text).group(1)
# redis_conn.set('qczj_city_str', city_items)
# redis_conn.hmset('qczj_city_dict', eval(city_items))

chars = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
         'O', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'X', 'Y', 'Z', ]

urls = ['https://www.autohome.com.cn/grade/carhtml/{}.html'.format(c) for c in chars]


def get_page(urls):
    for url in urls:
        response = get_response(url)
        yield response


def save_car_series(response):
    doc = PyQuery(response.content.decode('gb18030', 'ignore'))
    doc.remove('li.dashline')
    for brand in doc('dl').items():
        brand_name = brand('dt > div > a').text()
        data = {brand_name: {}}
        series_count = len(list(brand('dd div.h3-tit')))
        for index in range(series_count):
            series_name = brand('dd .h3-tit').eq(index)('a').text()  # \31 59 > dd > div > a
            data[brand_name].update({series_name: {}})
            for car in brand('dd ul').eq(index)('li').items():
                car_name = car('h4 a').text()
                car_url = 'https:' + car('h4 a').attr.href
                if '暂无' in str(car):
                    car_price = '暂无'
                else:
                    car_price = car('div').eq(0).text()
                car_name = car_name.replace('.', '·')

                # data[brand_name][series_name].update({car_name: {'价格': car_price, 'source_url': car_url, '具体款式':detail}})
                data[brand_name][series_name].update({car_name: {'价格': car_price, 'source_url': car_url}})
        mongo_conn.save(data, CONFIG_MONGO['table'] + 'qczj')
        # redis_conn.hset('qczj_car', brand_name, data)


def get_brand_urls(response):
    doc = PyQuery(response.content)
    dl = doc('.tab-content-item current div.uibox-con.rank-list.rank-list-pic dl')
    for car in dl.items():
        # 样例https://car.autohome.com.cn/price/brand-33-9.html#pvareaid=2042363
        brand_url = car('a').attr.href
        brand_name = car('')
        redis_conn.sadd('qczj_brand_urls', 'https:' + brand_url)


def get_series_urls(url):
    response = get_response(url)
    doc = PyQuery(response.content)
    list_cont = doc('.tab-content-item.current .list-cont')
    brand_name = doc('h2 a').text()
    for car in list_cont.items():
        # 样例https://car.autohome.com.cn/price/series-3170.html#pvareaid=2042207
        series_url = "https://car.autohome.com.cn" + car('.list-cont-main .main-title a').attr.href
        series_name = car('.list-cont-main .main-title a').text()
        redis_conn.sadd('qczj_series_urls', series_url)
    next_page = doc('.page-item-next').attr.href
    if next_page != 'javascript:void(0)':
        get_series_urls(next_page)


def get_style_url(response):
    doc = PyQuery(response.content)
    series_url =doc('.main-title a').attr.href
    series_name = doc('.main-title a').text()
    series_price = doc('.font-arial').text()
    car_type = doc('.interval01')
    for car in car_type.items():
        type_name = car('.interval01-list-cars-text').text()
        for li in car('.interval01-list li').items():
            # 样例https://www.autohome.com.cn/spec/36622/#pvareaid=2042128
            style_url = li('div p').eq(0)('a').attr.href
            style_name = li('div p').eq(0)('a').attr.href


def parse_detail_page(response):
    doc = PyQuery(response.content)
    car_detail_name = doc('h2')
    information = doc('.information-summary')
    price = {
        '经销商报价': information('#cityDealerPrice').text(),
        '厂商指导价': information('.factoryprice').text().split('：')[-1],
        '二手车价格': information('.usedprice a').text(),
    }
    base_info = doc('.baseinfo-list li')
    msg = []
    for li in base_info.items():
        msg.append(li.text())
    msg = msg[:-1]


if __name__ == '__main__':
    for res in get_page(urls):
        save_car_series(res)
        break
