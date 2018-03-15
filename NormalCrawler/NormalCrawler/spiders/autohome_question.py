# !/usr/bin/env python
# -*- coding:utf-8 -*-

import logging
import fontTools
import re
import time
import traceback

from scrapy import Request
from scrapy import Spider


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
date_format = '%Y-%m-%d %H:%M:%S'


useful_url = "https://zhidao.autohome.com.cn/ajax/GetUsefulInfo?tid={tid}&rids={rids}&_={t}"
class_url = "https://zhidao.autohome.com.cn/ajax/ZhidaoForClubTopicMerge?tid={tid}"


class AutohomeQuestion(Spider):
    name = "autohome_question"
    custom_settings = {
        "DOWNLOAD_DELAY": 3,
        ""
        "DEFAULT_REQUEST_HEADERS": {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/57.0.2986.0 Safari/537.36',
        },
    }

    def start_requests(self):
        url = "https://zhidao.autohome.com.cn/list/b33/s4-1.html"
        yield Request(url, callback=self.parse_list, headers={"X-Forwarded-For": self.random_ip})

    def parse_list(self, response):
        logger.info('list url is {}'.format(response.url))

        hrefs = response.xpath('//ul[@class="qa-list-con"]//a/@href').extract()
        for href in hrefs:
            href = re.sub("http:", "https:", href)
            logger.info('will crawl detail url is {}'.format(href))
            yield Request(href, callback=self.parse_detail, headers={"X-Forwarded-For": self.random_ip})
        next_page = response.xpath('//a[@class="page-item-next"]/@href').extract_first()
        if next_page:
            next_url = response.urljoin(next_page)
            logger.info("will crawl next page {}".format(next_url))
            yield Request(next_url, callback=self.parse_list, headers={"X-Forwarded-For": self.random_ip})

    def parse_detail(self, response):
        logger.info('detail url is {}'.format(response.url))

        post_item = {}
        post_item["title"] = response.xpath('//div[@id="consnav"]/span[last()]/text()').extract_first()
        # post_item["first_floor_content"] = response.xpath('normalize-space(//div[@class="conttxt"])').extract_first()
        post_item["first_floor_content"] = self.get_text(response)
        post_item["second_floor_content"] = response.xpath(
            'normalize-space((//div[contains(@class, "x-reply")])[1])').extract_first()
        post_item["url"] = response.url
        tid = response.xpath('//div[contains(@name, "replyuseful")]/@data-tid').extract_first()
        rid = response.xpath('//div[contains(@name, "replyuseful")]/@data-rid').extract_first()

        # class
        cat_url = class_url.format(tid=tid)
        yield Request(cat_url, callback=self.parse_class, headers={"Referer": response.url},
                      meta={"post_item": post_item, "tid": tid, "rid": rid})

    def parse_ttf(self, response):
        pass

    def parse_class(self, response):
        pass
