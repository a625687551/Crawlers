#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from urllib.parse import quote_plus

from scrapy import Spider
from scrapy import Request
from NormalCrawler.NormalCrawler.items import CompanyItem


logger = logging.getLogger(__file__)
logger.setLevel(logging.INFO)
date_format = '%Y-%m-%d %H:%M:%S'


class TianyanSpider(Spider):
    name = "tianyancha"
    list_url = "https://www.tianyancha.com/search/p1?key={kw}"
    custom_settings = {
        "DOWNLOAD_DELAY": 3,
        "DEFAULT_REQUEST_HEADERS": {
            "Accept-Encoding": "gzip, deflate, sdch",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
        },
        "SPIDER_MIDDLEWARES": {
            'NormalCrawler.NormalCrawler.middlewares.RandomUserAgent': 543,
        }
    }

    def start_requests(self):
        # key_list = ["通信", "通讯", "汽车", "地产", "母婴", "电子", "服饰", "软件", "公共关系", "公关", "数码"]
        key_list = ["批发零售", "餐饮", "住宿", "建材", "商贸", "美容院", "艾灸", "教育培训"]
        for kw in key_list:
            logger.info(u"search keyword {}".format(kw))
            kw = quote_plus(kw)
            yield Request(url=self.list_url.format(kw=kw), callback=self.parse_list, meta={"page": 1})

    def parse_list(self, response):
        page = response.meta["page"]
        info_list = response.xpath('//div[@class="search_right_item"]')

        for info in info_list:
            url = info.xpath("./div/a/@href").extract_first()
            name = info.xpath("normalize-space(./div/a/span)").extract_first()
            logger.info(u"will crawl detail page {} {}".format(name, url))
            yield Request(url=url, callback=self.parse_detail)

        if response.xpath('//li/a[contains(./text(),">")]') and page < 5:
            logger.info("next page")
            next_page_url = response.xpath('//li/a[contains(./text(),">")]/@href').extract_first()
            yield Request(url=next_page_url, callback=self.parse_list, meta={"page": page})

    def parse_detail(self, response):
        if response.status > 400:
            logger.info("page problem {}".format(response.url))
            return

        post_item = CompanyItem({
            "company_name": response.xpath(
                '//span[@class="f18 in-block vertival-middle sec-c2"]/text()').extract_first(),
            "company_phone": response.xpath(
                '//div[@class="f14 sec-c2 mt10"]/div[contains(@class,"mr20")]/span[2]/text()').extract_first(),
            "company_email": response.xpath('//div/div/span[contains(@class,"email")]/text()').extract_first(),
            "company_address": response.xpath('//div/div/span[contains(@class,"pr10")]/text()').extract_first(),
            "url": response.url,
        })
        logger.info("crawl one company ")
        yield post_item
