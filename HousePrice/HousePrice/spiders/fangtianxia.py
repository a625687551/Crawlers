# -*- coding: utf-8 -*-

import time
import logging
import sys
import re
import json
import os
import random
from urllib.parse import quote_plus

from scrapy import Spider
from scrapy import Request

base_url = "http://esf.sjz.fang.com"
detail_tem = "http://{}.fang.com/xiangqing/"
area_list = [
    "/housing/__0_0_0_0_1_0_0_0/"
    "/housing/357__0_0_0_0_1_0_0_0/"
    "/housing/359__0_0_0_0_1_0_0_0/"
    "/housing/358__0_0_0_0_1_0_0_0/"
    "/housing/360__0_0_0_0_1_0_0_0/"
    "/housing/361__0_0_0_0_1_0_0_0/"
    "/housing/628__0_0_0_0_1_0_0_0/"
    "/housing/629__0_0_0_0_1_0_0_0/"
    "/housing/630__0_0_0_0_1_0_0_0/"
    "/housing/632__0_0_0_0_1_0_0_0/"
    "/housing/10114__0_0_0_0_1_0_0_0/"
]


class Fangtianxia(Spider):
    name = "fangtianxia"

    def start_requests(self):
        for area in area_list:
            list_url = base_url + area
            yield Request(list_url, callback=self.parse_list, meta={"area": area})

    def parse_list(self, response):
        content = response.xpath('//div[@class="houseList"]/div[@class="list rel"]/dl')
        for single in content:
            detail_url = single.xpath('./dt/a/@href').re_first("http://(.*?).fang.com/")
            detail_url = detail_tem.format(detail_url)
            yield Request(detail_url, callback=self.parse_detail)

    def parse_detail(self, response):
        content = response.xpath('//div[@class="con clearfix"]')

