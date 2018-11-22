#!/usr/bin/env python
# -*- coding: utf-8 -*-
#   @CreateTime    : 2018/11/21 18:36
#   @Author  : yanwj
#   @File    : qczj.py
import re

from pyquery import PyQuery
from Tools.db_tools.mongo_tools import MongoClientTools
from Tools.db_tools.redis_tools import RedisConnection
from Tools.http_tools import get_response
from config import CONFIG_REDIS, CONFIG_MONGO

SOURCE = 'qczj'

CAR_RANK = {
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
CHARS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
         'O', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'X', 'Y', 'Z', ]


class AutoHome:
    def __init__(self):
        self.redis_conn = RedisConnection().redis_connect(**CONFIG_REDIS)
        self.mongo_conn = MongoClientTools(**CONFIG_MONGO)
        self.start_urls = ['https://www.autohome.com.cn/grade/carhtml/{}.html'.format(c) for c in CHARS]
        self.cityid = self.get_cityId()

    def get_brand_urls(self, url):
        response = get_response(url)
        doc = PyQuery(response.content.decode('gb18030', 'ignore'))
        car_data = {}
        for brand in doc('dl').items():
            brand_name = brand('dt > div > a').text()
            brand_url = brand('dt > div > a').attr.href
            if 'pic/' in brand_url:
                continue
            car_data.update({brand_name: {'source_url': 'https:' + brand_url}})
        return car_data

        # doc = PyQuery(response.contentdecode('gb18030', 'ignore'))
        # dl = doc('.tab-content-item current div.uibox-con.rank-list.rank-list-pic dl')
        # for car in dl.items():
        #     # 样例h ttps://car.autohome.com.cn/price/brand-33-9.html#pvareaid=2042363
        #     brand_url = car('a').attr.href
        #     brand_name = car('')
        #     if self.data.get(brand_name, None):
        #         pass
        #     else:
        #         self.data.update({brand_name:{}})

        # self.redis_conn.sadd('qczj_brand_urls', 'https:' + brand_url)

    def get_series_urls(self, car_data):
        data = {}
        for brand_name, v in car_data.items():
            response = get_response(v['source_url'])
            doc = PyQuery(response.content.decode('gb18030', 'ignore'))
            list_dl = doc('.carbrand dl')
            data1 = {}
            for dl in list_dl.items():
                # 一汽大众
                brand_name_type = dl('dt a').text()
                # brand_name_type_url = dl('dt a').attr.href
                counts = len(list(dl('dd div.list-dl-name')))
                data2 = {}
                for index in range(counts):
                    # 轿车
                    name_type = dl('dd div.list-dl-name').eq(index).text()
                    series_names = dl('dd div.list-dl-text').eq(index)('a')
                    data3 = {}
                    for series in series_names.items():
                        # 奥迪A3
                        series_name = series('a').text()
                        series_name_url = 'https://car.autohome.com.cn' + series('a').attr.href
                        series_detail = self.get_style_url(series_name_url)
                        data3.update({series_name.replace('.', '·'): {'series_url': series_name_url}})
                        data3.update({series_name.replace('.', '·'): series_detail})
                        break
                    data2.update({name_type.replace('.', '·'): data3})
                    break
                data1.update({brand_name_type.replace('.', '·'): data2})
                break
            data.update({brand_name.replace('.', '·'): data1})
            break
        return data
        # list_cont = doc('.tab-content-item.current .list-cont')
        # brand_name = doc('h2 a').text()
        # for car in list_cont.items():
        #     # 样例https://car.autohome.com.cn/price/series-3170.html#pvareaid=2042207
        #     series_url = "https://car.autohome.com.cn" + car('.list-cont-main .main-title a').attr.href
        #     series_name = car('.list-cont-main .main-title a').text()
        #     self.redis_conn.sadd('qczj_series_urls', series_url)
        # next_page = doc('.page-item-next').attr.href
        # if next_page != 'javascript:void(0)':
        #     self.get_series_urls(next_page)

    def get_style_url(self, url):
        response = get_response(url)
        doc = PyQuery(response.content.decode('gb18030', 'ignore'))
        series_price = doc('.font-arial').text()
        car_type = doc('.interval01')
        data = {}
        for car in car_type.items():
            type_name = car('.interval01-list-cars-text').text().replace('.', '·')
            data1 = {}
            for li in car('.interval01-list li').items():
                # 样例https://www.autohome.com.cn/spec/36622/#pvareaid=2042128
                style_url = 'https:' + li('div p').eq(0)('a').attr.href
                style_name = li('div p').eq(0)('a').text().replace('.', '·')
                spec_id = li.attr('data-value')
                detail = self.parse_detail_page(style_url, spec_id)
                data1.update({style_name: {'style_utl': style_url}})
                data1.update({style_name: detail})
                break
            data.update({type_name: data1})
            break
        data.update({'指导价格': series_price})
        return data

    def parse_detail_page(self, url, spec_id):
        response = get_response(url)
        doc = PyQuery(response.content.decode('gb18030', 'ignore'))
        information = doc('.information-summary')
        price = {
            '经销商报价': self.get_price(spec_id),
            '厂商指导价': information('.factoryprice').text().split('：')[-1],
            '二手车价格': information('.usedprice a').text(),
        }
        base_info = doc('.baseinfo-list li')
        msg = []
        for li in base_info.items():
            msg.append(li.text())
        msg = msg[:-1]
        price.update({'详情': msg})
        return price

    def get_price(self, spec_id):
        result = {}
        urls = {
            city: 'https://www.autohome.com.cn/ashx/dealer/AjaxDealerGetSpecsMinPrice.ashx?specids={}&cityid={}'.format(
                spec_id, cityid) for city, cityid in self.cityid.items()}
        for city, url in urls.items():
            json_data = get_response(url).json()
            try:
                price = json_data['result']['list'][0]['newsPrice']
            except Exception as e:
                print(city, '没有%s的价格' % spec_id)
                price = 0
            result.update({city: price})
            break
        return result

    def get_cityId(self):
        key = 'a00'
        url = 'https://www.autohome.com.cn/{}/'.format(key)
        res = get_response(url)
        city_items = re.search('<script language="javascript" type="text/javascript">var CityItems = (.*?);</script>',
                               res.text).group(1)

        city_items = {item['N']: item['I'] for item in eval(city_items)['CityItems']}
        # self.redis_conn.hmset('qczj_cityid', city_items)
        return city_items

    def run(self):
        cars = map(self.get_brand_urls, self.start_urls)
        result = map(self.get_series_urls, cars)
        [self.mongo_conn.save(item, CONFIG_MONGO['table'] + SOURCE) for item in result]


if __name__ == '__main__':
    qczj = AutoHome()
    qczj.run()
    # print(qczj.get_cityId())
