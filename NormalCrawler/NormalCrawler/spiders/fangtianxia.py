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

from NormalCrawler.NormalCrawler.items import HousepriceItem

base_url = "http://esf.sjz.fang.com"
detail_tem = "http://{}.fang.com/xiangqing/"
area_list = [
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
        info_item = HousepriceItem({
            "city_name": u"石家庄",
            "house_name": content.xpath('//a[@class="tt"]/text()').extract_first,
            "house_url": response.url,
            "house_address": content.xpath('').extract_first,
            "house_area": content.xpath('').extract_first,
            "house_price": content.xpath('').extract_first,
            "post_code": content.xpath('').extract_first,
            "cycle_area": content.xpath('').extract_first,
            "property_right": content.xpath('').extract_first,
            "category": content.xpath('').extract_first,
            "house_year": content.xpath('').extract_first,
            "house_structure": content.xpath('').extract_first,
            "house_type": content.xpath('').extract_first,
            "house_num": content.xpath('').extract_first,
            "building_num": content.xpath('').extract_first,
            "property_company": content.xpath('').extract_first,
            "green_rate": content.xpath('').extract_first,
            "volume_rate": content.xpath('').extract_first,
            "property_cellphone": content.xpath('').extract_first,
            "property_cost": content.xpath('').extract_first,
            "support_facility": content.xpath('').extract_first,
            "bad_thing": content.xpath('').extract_first,
            "traffic_condition": content.xpath('').extract_first,
            "surround_info": content.xpath('').extract_first,
        })
        yield info_item

