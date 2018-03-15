#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import logging
import sys
from urllib.parse import quote_plus

from lxml import etree
from scrapy import Spider
from scrapy import Request
from NormalCrawler.NormalCrawler.items import TiebaItem

logger = logging.getLogger(__file__)
logger.setLevel(logging.INFO)
date_format = '%Y-%m-%d %H:%M:%S'
reload(sys)
sys.setdefaultencoding('utf8')


class TiebaSpider(Spider):
    name = "tieba_info"

    def start_requests(self):
        with open("tieba_list.txt", "r") as f:
            for x in f.readlines():
                for i in ["&st=new", "&st=popular"]:
                    s = x.split(",")
                    category = s[0]
                    cate_url = s[1] + i
                    tag = s[2]
                    logger.info(u'will crawl tieba category name {} url {}'.format(category, cate_url))
                    yield Request(cate_url, priority=10, callback=self.parse_tieba_list,
                                  meta={'page': 0, "tag": tag, 'category': category})
        with open("tieba_url.txt", "r") as f:
            for x in f.readlines():
                s = x.decode("gbk", "ignore").split(",")
                category = s[0]
                cate_url = s[1]
                name = s[2]
                logger.info(u'will crawl tieba url name {} url {}'.format(category, cate_url))
                yield Request(cate_url, priority=10, callback=self.parse_tieba_info,
                              meta={'page': 0, "name": name, 'category': category, 'url': cate_url})

    def parse_tieba_list(self, response):
        page = response.meta["page"]
        category = response.meta["category"]
        tag = response.meta["tag"]
        source = response.xpath('//*[@class="ba_list clearfix"]/div')

        for post_info in source:
            post_item = TiebaItem()
            post_item["tieba_name"] = post_info.xpath('.//p[@class="ba_name"]/text()').extract_first()
            post_item["tieba_url"] = response.urljoin(post_info.xpath('./a/@href').extract_first())
            post_item["category"] = category
            post_item["baidu_tag"] = tag
            post_item["mem_num"] = post_info.xpath('.//span[@class="ba_m_num"]/text()').extract_first()
            post_item["post_num"] = post_info.xpath('.//span[@class="ba_p_num"]/text()').extract_first()
            yield post_item
            logger.info(post_item)
            logger.info(u'crawl tieba {}'.format(post_item["tieba_name"]))

        if page < 30 and response.xpath('//div[@class="pagination"]/a[@class="next"]/@href').extract_first():
            page += 1
            next_url = response.urljoin(response.xpath('//div[@class="pagination"]/a[@class="next"]/@href').extract_first())
            logger.info(u'will crawl tieba category name {} url {}'.format(category, next_url))
            yield Request(next_url, priority=10, callback=self.parse_tieba_list,
                          meta={'page': page, "tag": tag, 'category': category})

    def parse_tieba_info(self, response):
        if response.xpath('//div[@id="forum_not_exist"]'):
            logger.info(u"该贴吧有问题 {}".format(response.url))
            return

        category = response.meta["category"]
        name = response.meta["name"]
        url = response.meta['url']
        html = etree.HTML(response.body.replace("<!--", "").replace("-->", ""))

        post_item = TiebaItem()
        post_item["tieba_name"] = name
        post_item["tieba_url"] = url
        post_item["category"] = category
        post_item["baidu_tag"] = ""
        post_item["mem_num"] = html.xpath('//*[@class="card_menNum"]/text()')[0]
        post_item["post_num"] = html.xpath('//*[@class="card_infoNum"]/text()')[0]
        yield post_item
        logger.info(u'crawl tieba {}'.format(post_item["tieba_name"]))
