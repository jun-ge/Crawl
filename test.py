#!/usr/bin/env python
# -*- coding: utf-8 -*-
#   @CreateTime    : 2018/11/7 15:07
#   @Author  : yanwj
#   @File    : test1.py

# from Tools.db_tools.mongo_tools import MongoClientTools
# from config import CONFIG_MONGO_LOCAL
#
# conn = MongoClientTools()
# result = conn.search('tjgb', {'链接': 'http://www.tjcn.org/tjgb/26xz/35695.html'})
# print(list(result)[0].get('正文a', None))
#
# for item in result:
#     print(item['链接'])
# if result:
#     print('find it')
# from tjgb_total import get_detail_page
#
# get_detail_page('安徽', 'http://www.tjcn.org/tjgb/12ah/20390.html')
# print(chr(16*14+9))
import json
import logging
import re
import time
from _md5 import md5
from datetime import datetime, timedelta

# start_date = datetime(datetime.now().year, datetime.now().month, datetime.now().day)
# hours_now = datetime.now().hour
# if hours_now > 12:
#     history_days = [(start_date - timedelta(1 + n)).strftime('%Y-%m-%d') for n in range(7)]
# else:
#     history_days = [(start_date - timedelta(2 + n)).strftime('%Y-%m-%d') for n in range(7)]
#
# print(history_days)
# day_rank = "/xdnphb/list/{0}/rank?AppKey=joker&end={1}&rank_name={2}&rank_name_group={3}&start={4}&nonce="
# day_rank = day_rank.format('1','2','3','3','5')
# print(day_rank)
# print(((datetime.now()-timedelta(2)).weekday()))
# from urllib.parse import quote
from math import cos
from urllib.parse import quote

import js2py
import requests

# #
# #
# # url = 'https://www.baidu.com/我爱你'
# # print(quote(url))
# import threadpool
#
# res = requests.get(
#     'https://www.newrank.cn/xdnphb/list/day/rank?end=2018-11-11&rank_name=%E6%97%B6%E4%BA%8B&rank_name_group=%E8%B5%84%E8%AE%AF&start=2018-11-11&nonce=4c883d067&xyz=ced6aaac9320e8c28159b45fd88a7009')
#
# l = []
# # print(res.json())
#
# def a(n):
#     return n ** 2
#
#
# def callback(request, result):
#     print(result, request)
#     l.append(result)
#
#
# pool = threadpool.ThreadPool(5)
# queue = threadpool.makeRequests(a, [1, 2, 3, 4, 5], callback=callback)
# [pool.putRequest(item) for item in queue]
# pool.wait()
#
# # print(l)
# print(md5('/xdnphb/list/day/rank?AppKey=joker&end=2018-11-09&rank_name=百科&rank_name_group=资讯&start=2018-11-09&nonce='))
# response = requests.get('https://www.newrank.cn/public/info/list.html?period=week&type=data')
# # print(response.text)
# from pyquery import PyQuery
# doc = PyQuery(response.content)
# print(doc('#stat_num').text().strip())
from pyquery import PyQuery

from Tools.db_tools.mongo_tools import MongoClientTools

# date = json_str['value']['datas']
# sum = 0
# for item in date:
#     sum += int(item['g'])
# print(time.time())

# import math
# print(math.radom())
# import js2py
#
# flag = js2py.eval_js(
#
#     '''
#     x = function(){
#     var codeFlag = (new Date).getTime()+ "" + Math.random();  return codeFlag
#     };
#      x()''')
# print(flag)
# print(time.time())
# lis = []
# conn = MongoClientTools()
# result = conn.search('WeChat_OffiAccot_Rank', '详情')
# for item in result:
#     for account in item['datas']:
#         lis.append(account['account'])
#
# print(len(lis), len(set(lis)))
#
# headers = {
#
#     'cookie':'UM_distinctid=1671050654379b-0a766e0df90cd4-4313362-1fa400-1671050654455d; __root_domain_v=.newrank.cn; _qddaz=QD.1egnqi.adg2id.jogme5ge; rmbuser=true; name=13072761557; useLoginAccount=true; Hm_lvt_a19fd7224d30e3c8a6558dcb38c4beed=1542245983,1542251884,1542251909,1542253064; CNZZDATA1253878005=2021127788-1542165478-https%253A%252F%252Fwww.newrank.cn%252F%7C1542257304; token=40EB91D2AA5149E9ED4BE97AA1634359; _qddamta_2852150610=3-0; _qdda=3-1.3dd6x5; _qddab=3-bhfk13.joi72aow; Hm_lpvt_a19fd7224d30e3c8a6558dcb38c4beed=1542262380'
# }
#
# res = requests.get('https://www.newrank.cn/public/info/detail.html?account=quanshangcn',
#     # 'https://www.newrank.cn/xdnphb/data/weixinuser/searchWeixinDataByCondition?filter=tags&hasDeal=false&keyName=%E5%95%86%E4%B8%9A&order=NRI&nonce=0fbf79783&xyz=42e771a9eb71f222feed45ca7b7b9c4c',
#     cookies={'token':'40EB91D2AA5149E9ED4BE97AA1634359'},stream=True,verify=True,headers=headers)
# print(res.status_code)
# doc = PyQuery(res.content)
# for v in {
#             '简介': {
#                 '微信号': doc('p.info-detail-head-weixin-account.clearfix > span').eq(0).text().strip().split('：')[1],
#                 '公众号名称': doc('.info-detail-head-weixin-name span').text().strip().split(' ')[0],
#                 '功能介绍': doc('.info-detail-head-weixin-fun-introduce.ellipsis').attr.title,
#                 '是否原创': doc('.info-detail-original').text().strip(),
#                 '进入中国微信月榜500强次数': doc('.info-detail-500-tips.hover-chunk').text().strip().split('次')[0],
#                 '预估活跃粉丝': doc('.detail-fans-counts').text().strip(),
#                 '新榜分类': doc('a#info_detail_head_classify_type').text().strip(),
#                 'Tag': '|'.join([a.text().strip() for a in doc('.tag-name-list a')]),
#             },
#             '新榜指数': {
#                 '新榜指数': doc('div.info-detail-rank-indexing-rank-num span').text().strip(),
#                 '新榜排名': doc('div.info-detail-rank-indexing-rank-mc span').text().strip(),
#                 '统计时间': doc('div.info-detail-rank-indexing-rank-date span').text().strip(),
#
#             },
#             '发布数阅读量的统计数据': {
#                 '发布次数': doc('b#info_detail_rank_article_release_times').text().strip(),
#                 '发布篇数': doc('b#info_detail_rank_article_count').text().strip(),
#                 '10w+发布篇数': doc('b#info_detail_rank_article_count_big_clicks').text().strip(),
#                 '最高阅读量': doc('b#info_detail_rank_max_article_clicks_count').text().strip(),
#                 '阅读量-总计': doc('b#info_detail_rank_article_clicks_count'),
#                 '阅读量-平均': doc('b#info_detail_rank_avg_clicks_count').text().strip(),
#                 '头条阅读数-总计': doc('b#info_detail_rank_top_line').text().strip(),
#                 '头条阅读数-平均': doc('b#info_detail_rank_avg_top_line').text().strip(),
#                 '点赞数-总计': doc('b#info_detail_rank_article_likes_count').text().strip(),
#                 '点赞数-平均': doc('b#info_detail_rank_avg_article_likes_count').text().strip(),
#
#             },
#             '爬取时间': datetime.now().strftime('%Y-%m-%d %H:%S:%M'),
#         }.values():
#     if isinstance(v,str):
#         continue
#     for j,k in v.items():
#
#         print(j + '》：', k)


s = """


<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/html">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <meta HTTP-EQUIV="pragma" CONTENT="no-cache">
    <meta HTTP-EQUIV="Cache-Control" CONTENT="no-cache, must-revalidate">
    <meta HTTP-EQUIV="expires" CONTENT="0">
    <meta name="renderer" content="webkit">
    <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="mobile-web-app-capable" content="yes">
    <meta name="Description" content="券商中国（quanshangcn）,是新榜收录的微信公众号。通过对其长期的数据追踪并以新榜指数为依托对券商中国进行评估，方便新媒体从业者观测、学习。致力于提供最及时的财经资讯，最专业的解读分析，覆盖宏观经济、金融机构、A股市场、上市公司、投资理财等财经领域。"/>
    <meta name="Keywords" content="quanshangcn,券商中国,新榜券商中国数据,新榜quanshangcn数据,内容创业}" />
    <title>券商中国quanshangcn新榜</title>
    <link href="/assets/css/bootstrap.min.css" rel="stylesheet" type="text/css">
    <link href="https://assets.newrank.cn/assets/common/css/common.css?t=1" rel="stylesheet" type="text/css">
    <link href="/assets/css/info_detail.css?t=1" rel="stylesheet" type="text/css">
    <link href="/assets/css/pop.css?t=1" rel="stylesheet" type="text/css">
    <link href="/assets/js/lib/Datepicker/jquery-ui.css" rel="stylesheet" type="text/css" >
</head>
<body>
<div id="header"></div>
<!-- =====================================头部========================================================= -->
<div class="info-detail-root">
    <div class="info-detail-head">
        <div class="info-detail-head-weixin">
            <div class="info-detail-head-info">
                <div class="info-detail-head-weixin-head">
                    <div class="info-detail-head-weixin-img">
                        <span></span>
                    </div>
                    <div class="info-detail-head-weixin-yuan">
                        <span></span>
                    </div>
                    <div class="info-detail-head-weixin-ruzhu">
                        <span class="detail-pic"></span>
                    </div>
                </div>
                <div class="info-detail-head-weixin-medal">
                    <!-- <a href="javascript:;" title="添加到选号车"></a> -->
                    <div class="weixin_state invite-box detail-pic weixin_state-enquiry" data="1"></div>
                    <div class="weixin_state invite-box detail-pic weixin_state-no-bind" data="2"></div>
                    <div class="weixin_state invite-box detail-pic weixin_state-already-bind" data="3"></div>
                    <div class="weixin_state invite-box detail-pic weixin_state-immediately-bind" data="4"></div>
                    <div class="weixin_state invite-box detail-pic weixin_state-already-bind" data="5"></div>
                    <div class="weixin_state invite-box detail-pic weixin_state-immediately-bind" data="6"></div>
                </div>
            </div>
            <div class="info-detail-head-weixin-data" style="position:relative;">


                <div class="info-detail-head-weixin-name">
            	<span>券商中国
                    <!--<i id="detail_add_shopcar_no" class="detail-pic detail-add-shopcar-no" style=" display: none;" title="添加收藏"></i>
                    <i id="detail_add_shopcar_yes" class="detail-pic detail-add-shopcar-yes" style=" display: none;" title="取消收藏"></i>-->
            	</span>
                    <div class="cursor-p collect no-collect" >
                        <div class="hover-chunk collect-triangle"><p>点击即可<span class="collect-text">收藏</span>此公众号<br>可以去个人中心建立<a href="https://newrank.cn/account/user/ranklist.html" target="_blank" style="color:#00b0f0;text-decoration: none;">自定义榜单</a></p></div>
                    </div>
                    <div class="wx-code" style="">
                        <div class="hover-chunk wx-code-pic">
                            <img src="http://open.weixin.qq.com/qr/code?username=gh_6df2146bcb82" style="max-width:100%;"/>
                            <p style="font-size:12px;line-height:22px;margin-bottom:8px;">微信扫一扫关注</p>
                        </div>
                    </div>
                    <!--
        			<span class="info-detail-head-wxtop">500强</span>
        			<span class="info-detail-head-wxtop">原创</span>
-->

                    <!--<div class="info-detail-head-wx-detail">
                        <h3>-->
                    <!-- <p class="bdsharebuttonbox">
                        <a href="#" class="bds-more" data-cmd="more" title="点击即可进行分享"></a>
                    </p> -->
                    <!--<div class="info-detail-head-send-weixin">
			            	<span id="weixin_example" class="footer-pic"></span>
			                <img id="weixin_code" src="http://open.weixin.qq.com/qr/code/?username=gh_6df2146bcb82">-->
                    <!-- <div id="weixin_gz" class="info-detail-head-send-weixin-name"><span>关注</span></div> -->
                    <!--<div id="weixin_code_hover"></div>
                </div>
            </h3>
        </div>-->
                </div>
                <div>
                    <div style="font-size:0;float:right;margin-top:-40px;">
                        <span class="wubai" style="margin-left: 16px;cursor: pointer;"></span>
                        <div class="info-detail-500-tips hover-chunk" style="display: none;">11次进入中国微信月榜500强</div>
                    </div>
                    <div style="overflow:hidden;">
                        <div class="info-detail-head-weixin-num">
                            <p class="info-detail-head-weixin-account clearfix"><span>微信号：quanshangcn</span>
                                <!--<span class="info-detail-head-server"> -->
                                <span class="info-detail-original" style="font-size:12px;color:#999;border:1px solid #e3e3e3;border-radius:10px;line-height:16px;height:18px;margin-right:6px;margin-top:2px;" title="近期发布过原创内容的公众号">原创
                                    <!--<span class="info-detail-original-tips hover-chunk" style="top:18px;display: none;left:-15px;width: 182px; padding: 1px 3px;">近期发布过原创内容的公众号</span>--></span>



                                <!--</span>-->
                                <!--<span class="detail-enter-date">加入新榜时间：<span>2016-01-17 </span></span>-->

                            </p>
                            <p class="info-detail-head-weixin-approve ellipsis"><span title="微信认证：深圳证券时报社有限公司">
                            微信认证：深圳证券时报社有限公司
                </span></p>
                            <p class="info-detail-head-weixin-fun-introduce ellipsis" title="致力于提供最及时的财经资讯，最专业的解读分析，覆盖宏观经济、金融机构、A股市场、上市公司、投资理财等财经领域。">简介：<span>
                            致力于提供最及时的财经资讯，最专业的解读分析，覆盖宏观经济、金...
                </span></p>
                        </div></div></div>
            </div>
            <div class="info-detail-head-dist">
                <!-- <ul class="detail-dist">
                       <li>原创</li>
                       <li>赞赏</li>
                       <li>500强</li>
                       <li>广点通</li>
                   </ul> -->
                <div class="info-detail-head-fans">
                    <div class="detail-fans-counts" data="335,961">

                    335,961
                    </div>
                    <div class="detail-fans-img"><i class="detail-pic" title="基于历史数据表现评估，仅供参考"></i>预估活跃粉丝</div>
                    <div style="position:absolute;left:410px;bottom:10px;font-size:12px;width:152px;color:#B9B9B9;">加入新榜时间：<span>2016-01-17 </span></div>
                </div>
            </div>
        </div>
        <div class="info-detail-head-private-letter">
            <div class="info-detail-head-private-letter-img">
                <!-- <div class="info-detail-head-send-email"></div> -->
                <!-- 马上认领 -->
                <!-- <div id="weixin_state" class="invite-box"></div> -->
                <div class="tow-media">全平台</div>
                <div class="tow-mdia-list">
                    <ul></ul>
                </div>
            </div>
        </div>
        <div class="info-detail-head-line"></div>
        <div class="info-detail-head-classify">
            <p class="info-detail-head-classify-name"><span>新榜分类</span></p>
            <p class="info-detail-head-classify-subname"><a id="info_detail_head_classify_type" href="" target="_blank"></a></p>
            <div class="detail-tag">
                <div class="tag-name">标签</div>
                <ul class="tag-name-list"></ul>
            </div>
        </div>
        <div class="info-detail-head-line"></div>
    </div>
    <!-- ====================================标签切换================================================= -->
    <div class="info-detail-tab">
        <div class="info-detail-tab-buttons">
            <button class="info-detail-head-button-rank info-detail-tab-buttons-change" isChange="false" flag="rank"><span>排行</span></button>
            <!-- <button class="info-detail-tab-button-article" isChange="true" flag="article"><span>文章</span></button> -->
            <button class="info-detail-tab-button-ad-val" isChange="true" flag="av-val"><span>广告价值</span></button>
            <div id="info-detail-value" class="info-detail-value">
                <div id="info-detail-userface-cancle" class="cancle"><i class="detail-pic"></i></div>
                <div class="userface-img detail-pic"></div>
            </div>
        </div>
    </div>
    <!-- =====================================排行=================================================== -->
    <div class="info-detail-tab-rank" >

        <div class="info-detail-rank-indexing">
            <div class="info-detail-rank-indexing-change-info">
                <div class="info-detail-rank-indexing-change-drawing"></div>
                <div class="info-detail-rank-indexing-change-name"><span>新榜指数变化</span></div>
            </div>
            <div class="info-detail-rank-indexing-info">
                <div class="info-detail-rank-indexing-rank">
                    <div class="info-detail-rank-indexing-rank-date">
                        <span></span>
                    </div>
                    <div class="info-detail-rank-indexing-rank-detail">
                        <div class="info-detail-rank-indexing-rank-name"><span>新榜指数</span></div>
                        <div class="info-detail-rank-indexing-rank-num"><span></span></div>
                        <div class="info-detail-rank-indexing-rank-mc"><span>第0名</span></div>
                        <div class="info-detail-rank-indexing-omit-data"></div>
                    </div>
                </div>
                <div class="info-detail-rank-indexing-list">
                    <div class="info-detail-rank-indexing-list-data">
                        <div class="info-detail-rank-indexing-top">
                            <div class="info-detail-rank-indexing-top-name"><span>最近30天最高指数</span></div>
                            <div class="info-detail-rank-indexing-top-num">
                        	<span id="info_detail_rank_max_index_num">
                            947
                        	</span>
                            </div>
                        </div>
                        <div class="info-detail-rank-indexing-date">
                            <div class="info-detail-rank-indexing-top-name"><span>发生在</span></div>
                            <div class="info-detail-rank-indexing-top-num">
                        	<span id="info_detail_rank_max_index_date">
	                        		2018-10-23
	                        </span>
                            </div>
                        </div>
                    </div>
                    <div class="info-detail-rank-indexing-white-line"></div>
                    <div class="info-detail-rank-indexing-list-data">
                        <div class="info-detail-rank-indexing-top">
                            <div class="info-detail-rank-indexing-top-name"><span>最近30天最高日排名</span></div>
                            <div class="info-detail-rank-indexing-top-num"><span id="info_detail_rank_max_rank_num">第3名</span></div>
                        </div>
                        <div class="info-detail-rank-indexing-date">
                            <div class="info-detail-rank-indexing-top-name"><span>发生在</span></div>
                            <div class="info-detail-rank-indexing-top-num">
                        	<span id="info_detail_rank_max_rank_date">
                        			2018-11-08
                        	</span>
                            </div>
                        </div>
                    </div>
                    <div class="info-detail-rank-indexing-gray-line"></div>
                    <div class="info-detail-rank-indexing-list-operation">
                        <div class="info-detail-rank-indexing-list-img"><a id="weixin_skip_bang" target="_blank">财富日榜</a></div>
                    </div>
                </div>
            </div>
        </div>
        <div class="info-detail-rank-statistics">
            <ul class="info-detail-rank-fb">
                <li class="first">
                    <h3>发布次数</h3>
                    <p><b id="info_detail_rank_article_release_times"></b>次</p>
                </li>
                <li>
                    <h3>发布篇数</h3>
                    <p><b id="info_detail_rank_article_count"></b>篇</p>
                </li>
                <li>
                    <h3>10w+发布</h3>
                    <p><b id="info_detail_rank_article_count_big_clicks"></b>篇</p>
                </li>
                <li class="last">
                    <h3>最高阅读数</h3>
                    <p><b id="info_detail_rank_max_article_clicks_count"></b></p>
                </li>
            </ul>
            <div class="info-detail-rank-rule">
                <div class="info-detail-rank-rule-txt">
                    <p class="lj">总计</p>
                    <p class="pj">平均</p>
                </div>
                <ul class="info-detail-rank-rule-num">
                    <li>
                        <h4><img src="/assets/img/other/yds.jpg"></h4>
                        <p id="info_detail_rank_article_clicks_count" class="info-detail-article-clicks-count"></p>
                        <p id="info_detail_rank_avg_clicks_count" class="average"></p>
                    </li>
                    <li>
                        <h4><img src="/assets/img/other/ttyds.jpg"></h4>
                        <p id="info_detail_rank_top_line"></p>
                        <p id="info_detail_rank_avg_top_line" class="average"></p>
                    </li>
                    <li>
                        <h4><img src="/assets/img/other/dzs.jpg"></h4>
                        <p id="info_detail_rank_article_likes_count"></p>
                        <p id="info_detail_rank_avg_article_likes_count" class="average"></p>
                    </li>
                </ul>

            </div>
        </div>
        <div class="info-detail-rank-data-title">
            <i></i>数据统计
        </div>
        <div class="info-detail-rank-data-drawing">
            <div class="info-detail-rank-data-drawing-left">
                <div id="info_detail_rank_data_drawing_trend1" class="info-detail-rank-data-drawing-tab">
                    <h4 id="trend_rank_position" class="cur" name="排名变化">排名变化</h4>
                    <h4 id="trend_article_count" name="发布数">发布数</h4>
                </div>
                <div class="info-detail-rank-data-drawing-ranking"></div>
            </div>
            <div class="info-detail-rank-data-drawing-right">
                <div id="info_detail_rank_data_drawing_trend2" class="info-detail-rank-data-drawing-tab">
                    <h4 id="trend_article_clicks_count" class="cur" name="总阅读数">总阅读数</h4>
                    <h4 id="trend_article_clicks_count_top_line" name="头条阅读数">头条阅读数</h4>
                    <h4 id="trend_avg_article_clicks_count" name="平均阅读数">平均阅读数</h4>
                    <h4 id="trend_max_article_clicks_count" name="最高">最高</h4>
                    <h4 id="trend_article_likes_count" name="点赞数">点赞数</h4>
                </div>
                <div class="info-detail-rank-data-drawing-reading"></div>
            </div>
        </div>
    </div>
    <!-- ===========================================广告价值========================================== -->
    <div class="info-detail-tab-ad-val">
        <div id="info-detail-userface" class="info-detail-userface">
            <div class="tip">
                <i class="detail-pic"></i>
            </div>
            <div class="data" id="user_xinqu">
                <!-- <div class="img">
                    <i class="detail-pic woman"></i>
                    <i class="detail-pic man"></i>
                </div>
                <div id="scale_content" class="content">
                    <div id="scale_woman" class="woman"></div>
                    <div id="scale_man" class="man"></div>
                    <div class="scale">
                        <div id="scale_woman_num" class="scale-woman"></div>
                        <div id="scale_man_num" class="scale-man"></div>
                    </div>
                </div> -->
            </div>
            <div class="more">
                <a href="/public/info/userface.html?uuid=AE985326AAFA9FD1D4E23A394110CCEB" target="_blank">查看更多</a>
            </div>
        </div>
        <div class="info-detail-ad-fans-tip">
            <div class=title>“券商中国”运营方已于<span id="info_detail_ad_upload_date" ></span>上传后台显示粉丝数、性别比等相关数据，参见下方</div>
            <div class="hint"></div>
        </div>
        <div class="info-detail-ad-fans">
            <div class="has-data" id="ad-fans-has-data">
                <div class="image"></div>
                <div class="info-detail-ad-fans-data">
                </div>
                <div class="line"></div>
                <div class="info-detail-ad-fans-location">
                </div>
                <div class="info-detail-fans-show">
                    <img id="fans_show_img" />
                    <img id="jx_show_img" />
                    <img id="gender_show_img" />
                    <img id="provinces_show_img" />
                </div>
            </div>
            <div class="no-data" id="ad-fans-no-data">
                <div class="content">
                    <span class="img detail-pic"></span>
                    <span class="tips">“券商中国”运营方尚未上传后台显示粉丝数、性别比等相关数据</span>
                    <a class="upload" href="" target="_blank"><span>立即上传</span></a>
                </div>
            </div>
        </div>
        <div class="info-detail-ad-image-text-info">
            <div class="info-detail-ad-title-info">
                <div class="info-detail-ad-title-names">
                    <div class="info-detail-chosen-position"><span></span></div>
                    <ul class="info-detail-ad-title-names-list">
                        <!-- <li class="info-detail-ad-sign9" ><span>单图文</span></li>
                        <li class="info-detail-ad-more0"><span>多图文头条</span></li>
                        <li class="info-detail-ad-more1"><span>多图文2</span></li>
                        <li class="info-detail-ad-more2"><span>多图文3</span></li>
                        <li class="info-detail-ad-more3"><span>多图文4</span></li>
                        <li class="info-detail-ad-more4"><span>多图文5</span></li>
                        <li class="info-detail-ad-more5"><span>多图文6</span></li>
                        <li class="info-detail-ad-more6"><span>多图文7</span></li>
                        <li class="info-detail-ad-more7"><span>多图文8</span></li>
                        <li class="info-detail-ad-more8"><span>多图文末条</span></li> -->
                        <li class="info-detail-ad-sign0" ><span>全部</span></li>
                        <li class="info-detail-ad-more1"><span>单图文</span></li>
                        <li class="info-detail-ad-more2"><span>多图文头条</span></li>
                        <li class="info-detail-ad-more3"><span>多图文次条</span></li>
                        <li class="info-detail-ad-more4"><span>多图文3~N</span></li>
                        <!--<li class="info-detail-ad-more5"><span>最后一条</span></li>-->
                    </ul>
                </div>
                <div class="info-detail-ad-drawing">
                    <div class="info-detail-ad-drawing-left">
                        <div class="info-detail-ad-drawing-name1"><span>预期阅读</span></div>
                        <div class="info-detail-ad-drawing-name2"><span>发布概率</span></div>
                    </div>
                    <div class="info-detail-ad-drawing-line"></div>
                    <div class="info-detail-ad-drawing-right">
                        <div class="info-detail-ad-expect-reading"></div>
                        <div class="info-detail-ad-release-gl"></div>
                    </div>
                </div>
            </div>
            <div class="info-detail-ad-image-text-detail">
                <div class="info-detail-ad-more-first-text">
                    <p class="info-detail-ad-more-first-name"></p>
                    <div class="info-detail-ad-more-first-info">
                        <div class="info-detail-ad-more-first-tj">
                        <span class="num">
                        	<span id="ti_num"></span>
                        	<span class="unit"></span>
                        </span>
                            <span class="lable">预期阅读量</span>
                        </div>
                        <div class="info-detail-ad-more-first-tj-xq">
                            <p class="max">Max:<span class="max-num"></span>(+<span class="max-per"></span>)</p>
                            <p class="min">Min:<span class="min-num"></span>(-<span class="min-per"></span>)</p>
                        </div>
                    </div>
                </div>

                <div class="info-detail-ad-more-notes-text">
                    <div class="info-detail-ad-more-first-info">
                        <div class="info-detail-ad-more-first-tj">
                            <span id="notes_num" class="num">无记录</span>
                            <span class="lable">成交均价</span>
                        </div>
                        <div class="info-detail-ad-more-notes-price">
                            <span class="price"><span class="num"></span><span class="unit">元/千阅读</span></span>
                        </div>
                    </div>
                </div>
                <div class="info-detail-ad-more-statistics-text">
                    <p>该位置累计发布<span class="num"></span>次，占比<span class="percent"></span></p>
                </div>
            </div>
        </div>
        <div class="info-detail-ad-image-tj">
            <div class="info-detail-ad-image-hint"></div>
            <p class="info-detail-ad-image-tj-p">
                单图文：<span class="sign-num" id="single_fb_gl">0</span>%（<span class="sign-fb" id="single_fb_count">0</span>次发布）
                多图文：<span class="more-num" id="more_fb_gl">0</span>%（<span class="more-fb" id="more_fb_count">0</span>次发布）
                <span class="fb-avg-length-text">每次推送平均长度<span class="fb-avg-length-num"><span id="avg_fb_length">0</span>篇</span></span>
            </p>
        </div>
        <div class="info-detail-ad-quote-remark" style="background-color: #f2f2f2;height: 221px;padding: 8px;margin-top:25px;">
            <div class="info-detail-ad-remark" style="background-color: #fff;height: 180px;margin: 21px 10px;">
                <div class="info-detail-ad-remark-localtion">
                    <div class="localtion-name"><span>面向地域</span></div>
                    <div id="info_detail_ad_zone" class="localtion-content"></div>
                </div>
                <div class="info-detail-ad-bz">
                    <div class="bz-name"><span>备注信息</span></div>
                    <div id="info_detail_ad_advice" class="bz-content"></div>
                </div>
            </div>
        </div>
        <div class="info-detail-ad-action">
            <div class="image"></div>
            <div class="yuan">
           <span class="span-position">
               <span id="fate" class="num">0</span>
               <span class="unit">天</span>
           </span>
                <span id="fate_percent" class="percent" >0</span>
                <span class="yuan-name">活跃天数</span>
            </div>
            <div class="yuan">
           <span class="span-position">
               <span id="sheet_report" class="num">0</span>
               <span class="unit">篇</span>
           </span>
                <span id="sheet_report_percent" class="percent" >0</span>
                <span class="yuan-name">被举报或删除</span>
            </div>
            <div class="yuan">
           <span class="span-position">
               <span id="sheet_total" class="num">0</span>
               <span class="unit">篇</span>
           </span>
                <span id="sheet_total_percent" class="percent">0</span>
                <span class="yuan-name">10W+</span>
            </div>
        </div>
        <div class="info-detail-ad-hot-word">
            <div class="image"></div>
            <p class="hot-word-text"><span class="hot-word-name">热词</span></p>
            <ul class="info-detail-ad-hot-word-list"></ul>
            <div class="zwz"></div>
        </div>
        <div class="info-detail-ad-fb-time">
            <div class="image"></div>
            <p class="name">24小时发布趋势</p>
            <div class="info-detail-ad-fb-time-drawing"></div>
        </div>
    </div>
    <!-- ==================================文章====================================================== -->
    <div class="info-detail-article ">
        <div class="info-detail-article-top">
            <div class="hottest">
                <div class="top-title"><i></i>7天热门</div>
                <ul id="info_detail_article_top" class="info-detail-article-list"></ul>
            </div>
            <div class="newest">
                <div class="top-title"><i></i>最新发布 </div>
                <ul id="info_detail_article_lastest" class="info-detail-article-list"></ul>
            </div>
        </div>
    </div>
</div>

<!-- 询购  -->
<div class="tender-pop-box" style="display:none"></div>
<div class="detail-pop-box" style="display:none"></div>
<div class="detail-pop-allPlatform" style="display:none"></div> 

<div id="footer"></div>
<script type="text/javascript">
    var esbclf = {"data":[{"article_clicks_count":"341725","article_likes_count_top_line":"577","rank_name":"财富","insert_time":"2018-11-15 12:02:54.0","rank_position":"4","max_article_likes_count":"323","article_count_big_clicks":"0","avg_article_clicks_log1p_mark":"865.911364317768","uid":"192444","article_clicks_log1p_mark":"937.4204910253993","update_time":"2018-11-15 12:15:53.0","max_article_clicks_count":"90417","top_article_clicks_log1p_mark":"1063.4073009963513","article_likes_count":"1422","article_clicks_count_top_line":"207510","article_count":"16","rank_date":"2018-11-14 00:00:00.0","avg_article_clicks_count":"21357","id":"129681419","article_count_top_line":"3","max_article_clicks_log1p_mark":"991.2501183018504","new_rank_index_mark":"924.54462283905","avg_article_clicks_count_top_line":"69170","avg_article_likes_count_top_line":"192","avg_article_likes_count_other":"65","article_release_times":"3","avg_article_likes_count":"88","log1p_mark":"924.54462283905","name":"券商中国","avg_article_clicks_count_other":"10324","article_count_other":"13","rank_mark":"95.6419534035375","article_likes_count_other":"845","article_likes_log1p_mark":"643.1049434662726","account":"quanshangcn","article_clicks_count_other":"134215"},{"article_clicks_count":"353554","article_likes_count_top_line":"721","rank_name":"财富","insert_time":"2018-11-14 12:02:34.0","rank_position":"4","max_article_likes_count":"561","article_count_big_clicks":"0","avg_article_clicks_log1p_mark":"868.8698391607314","uid":"192444","article_clicks_log1p_mark":"939.9240881333401","update_time":"2018-11-14 12:15:28.0","max_article_clicks_count":"94741","top_article_clicks_log1p_mark":"1045.6955891267346","article_likes_count":"2054","article_clicks_count_top_line":"169231","article_count":"16","rank_date":"2018-11-13 00:00:00.0","avg_article_clicks_count":"22097","id":"129633992","article_count_top_line":"3","max_article_clicks_log1p_mark":"995.3076451768113","new_rank_index_mark":"927.6630728157601","avg_article_clicks_count_top_line":"56410","avg_article_likes_count_top_line":"240","avg_article_likes_count_other":"102","article_release_times":"3","avg_article_likes_count":"128","log1p_mark":"927.6630728157601","name":"券商中国","avg_article_clicks_count_other":"14178","article_count_other":"13","rank_mark":"95.92330681710149","article_likes_count_other":"1333","article_likes_log1p_mark":"675.6572216900896","account":"quanshangcn","article_clicks_count_other":"184323"},{"article_clicks_count":"343616","article_likes_count_top_line":"857","rank_name":"财富","insert_time":"2018-11-13 12:03:07.0","rank_position":"4","max_article_likes_count":"571","article_count_big_clicks":"1","avg_article_clicks_log1p_mark":"877.991844676964","uid":"192444","article_clicks_log1p_mark":"937.8264849296958","update_time":"2018-11-13 12:14:55.0","max_article_clicks_count":"100000","top_article_clicks_log1p_mark":"1060.627486222148","article_likes_count":"1893","article_clicks_count_top_line":"200974","article_count":"14","rank_date":"2018-11-12 00:00:00.0","avg_article_clicks_count":"24544","id":"129440888","article_count_top_line":"3","max_article_clicks_log1p_mark":"1000","new_rank_index_mark":"927.6219623079708","avg_article_clicks_count_top_line":"66991","avg_article_likes_count_top_line":"285","avg_article_likes_count_other":"94","article_release_times":"3","avg_article_likes_count":"135","log1p_mark":"927.6219623079708","name":"券商中国","avg_article_clicks_count_other":"12967","article_count_other":"11","rank_mark":"96.69717999873114","article_likes_count_other":"1036","article_likes_log1p_mark":"668.4307966379034","account":"quanshangcn","article_clicks_count_other":"142642"},{"article_clicks_count":"334308","article_likes_count_top_line":"698","rank_name":"财富","insert_time":"2018-11-12 12:03:54.0","rank_position":"4","max_article_likes_count":"322","article_count_big_clicks":"1","avg_article_clicks_log1p_mark":"869.6134644830963","uid":"192444","article_clicks_log1p_mark":"935.8060901381019","update_time":"2018-11-12 12:13:43.0","max_article_clicks_count":"100000","top_article_clicks_log1p_mark":"1060.5993895108497","article_likes_count":"1572","article_clicks_count_top_line":"200909","article_count":"15","rank_date":"2018-11-11 00:00:00.0","avg_article_clicks_count":"22287","id":"129317321","article_count_top_line":"3","max_article_clicks_log1p_mark":"1000","new_rank_index_mark":"924.4449709572482","avg_article_clicks_count_top_line":"66969","avg_article_likes_count_top_line":"232","avg_article_likes_count_other":"72","article_release_times":"3","avg_article_likes_count":"104","log1p_mark":"924.4449709572482","name":"券商中国","avg_article_clicks_count_other":"11116","article_count_other":"12","rank_mark":"96.8596768838166","article_likes_count_other":"874","article_likes_log1p_mark":"651.9817485963906","account":"quanshangcn","article_clicks_count_other":"133399"},{"article_clicks_count":"239170","article_likes_count_top_line":"517","rank_name":"财富","insert_time":"2018-11-11 12:03:48.0","rank_position":"5","max_article_likes_count":"357","article_count_big_clicks":"0","avg_article_clicks_log1p_mark":"840.524174649424","uid":"192444","article_clicks_log1p_mark":"911.1682248744216","update_time":"2018-11-11 12:13:37.0","max_article_clicks_count":"69010","top_article_clicks_log1p_mark":"1015.1252967880608","article_likes_count":"1238","article_clicks_count_top_line":"119022","article_count":"15","rank_date":"2018-11-10 00:00:00.0","avg_article_clicks_count":"15944","id":"129194004","article_count_top_line":"3","max_article_clicks_log1p_mark":"967.7828235129771","new_rank_index_mark":"898.116018592305","avg_article_clicks_count_top_line":"39674","avg_article_likes_count_top_line":"172","avg_article_likes_count_other":"60","article_release_times":"3","avg_article_likes_count":"82","log1p_mark":"898.116018592305","name":"券商中国","avg_article_clicks_count_other":"10012","article_count_other":"12","rank_mark":"94.78790156872596","article_likes_count_other":"721","article_likes_log1p_mark":"630.8405291298889","account":"quanshangcn","article_clicks_count_other":"120148"},{"article_clicks_count":"320104","article_likes_count_top_line":"655","rank_name":"财富","insert_time":"2018-11-10 12:03:17.0","rank_position":"5","max_article_likes_count":"329","article_count_big_clicks":"1","avg_article_clicks_log1p_mark":"854.969321390129","uid":"192444","article_clicks_log1p_mark":"932.6118971028815","update_time":"2018-11-10 12:16:32.0","max_article_clicks_count":"100000","top_article_clicks_log1p_mark":"1069.2497097931112","article_likes_count":"1323","article_clicks_count_top_line":"221948","article_count":"17","rank_date":"2018-11-09 00:00:00.0","avg_article_clicks_count":"18829","id":"129095703","article_count_top_line":"3","max_article_clicks_log1p_mark":"1000","new_rank_index_mark":"920.2542290166153","avg_article_clicks_count_top_line":"73982","avg_article_likes_count_top_line":"218","avg_article_likes_count_other":"47","article_release_times":"3","avg_article_likes_count":"77","log1p_mark":"920.2542290166153","name":"券商中国","avg_article_clicks_count_other":"7011","article_count_other":"14","rank_mark":"94.56078386792133","article_likes_count_other":"668","article_likes_log1p_mark":"636.7177712157156","account":"quanshangcn","article_clicks_count_other":"98156"},{"article_clicks_count":"378681","article_likes_count_top_line":"498","rank_name":"财富","insert_time":"2018-11-09 12:03:10.0","rank_position":"3","max_article_likes_count":"413","article_count_big_clicks":"1","avg_article_clicks_log1p_mark":"886.4294728403808","uid":"192444","article_clicks_log1p_mark":"944.9752860727301","update_time":"2018-11-09 12:14:24.0","max_article_clicks_count":"100000","top_article_clicks_log1p_mark":"1071.9073545641838","article_likes_count":"1361","article_clicks_count_top_line":"228844","article_count":"14","rank_date":"2018-11-08 00:00:00.0","avg_article_clicks_count":"27048","id":"128874337","article_count_top_line":"3","max_article_clicks_log1p_mark":"1000","new_rank_index_mark":"932.9309881696288","avg_article_clicks_count_top_line":"76281","avg_article_likes_count_top_line":"166","avg_article_likes_count_other":"78","article_release_times":"3","avg_article_likes_count":"97","log1p_mark":"932.9309881696288","name":"券商中国","avg_article_clicks_count_other":"13621","article_count_other":"11","rank_mark":"97.2850548289145","article_likes_count_other":"863","article_likes_log1p_mark":"639.2241720566797","account":"quanshangcn","article_clicks_count_other":"149837"}],"lastUpdateTime":"2018-11-14"};
    var fgkcdg = {"account_type":"0","wxu_status":"1","month_top_times":"11","description":"致力于提供最及时的财经资讯，最专业的解读分析，覆盖宏观经济、金融机构、A股市场、上市公司、投资理财等财经领域。","insert_time":"2016-01-17 20:18:51.0","type":"财富","uuid":"AE985326AAFA9FD1D4E23A394110CCEB","is_ori_user":"1","last_rank_position":"4","head_image_url":"http://mmbiz.qpic.cn/mmbiz/f23EOWYFfgHc5stQSqUHMdMlr2jdQu3AvcjGz5WyGVhnUvynzNNBv1SVOm6ftSiakibTUy49zjIRfkLfJ0jJTsqg/0","weixincodePath":"http://open.weixin.qq.com/qr/code?username\u003dgh_6df2146bcb82","certified_text":"微信认证：深圳证券时报社有限公司","name":"券商中国","id":"192444","wx_id":"gh_6df2146bcb82","account":"quanshangcn"};
    var trendSize = 7;
    var rankDayCount = 0;
    window.relativeUrl = '/';
</script>
<script src="https://assets.newrank.cn/assets/common/js/seajs-config-front.js"></script>
<script>
    seajs.use("/static/public/info/detail_new");
</script>
<div style="display: none;">
    <script type="text/javascript">var cnzz_protocol = (("https:" == document.location.protocol) ? " https://" : " http://");document.write(unescape("%3Cspan id='cnzz_stat_icon_1253878005'%3E%3C/span%3E%3Cscript src='" + cnzz_protocol + "s11.cnzz.com/z_stat.php%3Fid%3D1253878005' type='text/javascript'%3E%3C/script%3E"));</script>
</div>

</body>
</html>
"""


# esbclf = re.search('var esbclf = (.*?)lastUpdateTime":".*?}', s).group().replace('var esbclf =', '').strip()
# fgkcdg = re.search('var fgkcdg = (.*?)}', s).group().replace('var fgkcdg =', '').strip()
# print(esbclf)
# print(fgkcdg)
#
# s1 = "{'a':'b'}".replace('\'','\"')
# print(json.loads(s1))

# conn = MongoClientTools()
# account1 = set()
# data1 = conn.search('WeChat_OffiAccot_Rank', '详情')
# for item in data1:
#     for account in item['datas']:
#         account1.add(account['account'].lower())
# data2 = conn.search('WeChat_OffiAccot_Tag', '基本信息')
#
# account2 = set()
# for d in data2:
#     data2 = d['result']
#     for item2 in data2:
#         account2.add(item2['accountLower'])


#
# print(len(account1))
# print(len(account2))
# print(len(account2 | account1))
#
# print(account1.update(account2))
# print(len(account1))
# s1 = '"uuid=04205A9952E24C3292871BA9F0E2852B",,,,,"uuid=04205A9952E24C3292871BA9F0E2852B"'
# result = re.search('uuid=(.*?)"',s1).group(1)

class GetNewrankPWDJS:
    def __init__(self):
        with open('get_password.js', 'r', encoding='gb18030') as fr:
            self.js_code = fr.read()

        # .format('day', formdata['end'], formdata['rank_name'], formdata['rank_name_group'], formdata['start'])

    # 执行js文件获取nonce和xyz
    def run(self, parser_module):
        while True:
            try:
                return js2py.eval_js(self.js_code.replace('password', parser_module))
            except Exception as e:
                logging.info(parser_module + '加密错误', e)
                time.sleep(60)


if __name__ == '__main__':
    # pas = GetNewrankPWDJS()
    # print(pas.run('ywj13072761557'))

    # data_exist = list(conn.search('WeChat_OffiAccot_Info', 'source_url'))
    # print(data_exist)
    # res = requests.get('https://www.newrank.cn/public/login/login.html', auth=('18571869616', '123456'))
    # print(res.status_code)
    # print(res.cookies)
    # print(res.content.decode('utf-8'))
    # print(res.json())
    # a = [1, 2, 3, 4, 5]
    # print(a[::-1])
    from Tools.db_tools.redis_tools import RedisConnection
    from config import CONFIG_REDIS
    from Tools.db_tools.mongo_tools import MongoClientTools
    mongo_conn = MongoClientTools()
    redis_conn = RedisConnection().redis_connect(**CONFIG_REDIS)
    data1 = mongo_conn.search('WeChat_OffiAccot_Rank')
    for item in data1:
        redis_conn.sadd('newrank_time_range_filter', item['统计时间区间'])

    data2 = mongo_conn.search('WeChat_OffiAccot_Info')
    for item in data2:
        if item.get('wx_account', None):
            redis_conn.sadd('newrank_wx_account_filter', item['wx_account'])
