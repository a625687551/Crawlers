# -*- coding: utf-8 -*-
# import scrapy
import logging

from functools import reduce
from scrapy import Spider
from scrapy import Request
from urllib.parse import quote_plus

from CompanyCrawler.items import CompanycrawlerItem

logger = logging.getLogger(__file__)
logger.setLevel(logging.INFO)


class TianyanSpider(Spider):
    name = 'tianyan'
    allowed_domains = ['tianyancha.com']
    key_list = ["批发零售", "餐饮", "住宿", "建材", "商贸", "美容院", "艾灸", "教育培训"]
    base_url = "https://xingtai.tianyancha.com/search/p{pg}?key={kw}"

    def start_requests(self):
        for key in self.key_list:
            for pg in range(1, 6):
                list_url = self.base_url.format(pg=pg, kw=quote_plus(key))
                yield Request(url=list_url, callback=self.parse_list)

    def parse_list(self, response):
        content = response.xpath('//div[@class="search_right_item ml10"]/div/a/@href').extract()

        for cell in content:
            yield Request(url=cell, callback=self.parse_detail)

    def parse_detail(self, response):
        pass
