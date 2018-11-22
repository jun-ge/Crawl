#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  @CreateTime    : 2018/11/19 18:22
#  @Author  : yanwj
#  @File    : run.py
import logging
import os

from apps.newrank.newrank_rank import NewRank
from apps.newrank.newrank_tag import NewrankTag


newrank_tag = NewrankTag()
newrank_rank = NewRank()

if __name__ == '__main__':
    if not os.path.exists('./log'):
        os.mkdir('./log')
    logging.basicConfig(level=logging.INFO,
                        filemode="a",
                        filename="./log/newrank_info.log",
                        format='%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s', )

    # 榜单
    # new_rank.run()
    # 标签
    # newrank.run_tags()
    #info
    newrank_tag.run_tag_info()
