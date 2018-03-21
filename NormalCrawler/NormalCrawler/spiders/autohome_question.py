# !/usr/bin/env python
# -*- coding:utf-8 -*-

import re
import logging
import random
import json

from scrapy import Request
from scrapy import Spider

from .extract.parser import parse_kw

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

    def parse_class(self, response):
        logger.info('class url is {}'.format(response.url))
        post_item = response.meta["post_item"]
        tid = response.meta["tid"]
        rid = response.meta["rid"]

        data_list = re.findall(r"var qaextend = ({.*?});", response.body)
        if data_list:
            data = json.loads(data_list[0].decode("gbk"))
            # result = " > ".join(
            #     map(lambda x: data.get(x, "").strip(), ["brandName", "seriesName", "class1Name", "class2Name"]))
            result = " > ".join(
                filter(None, map(lambda x: data.get(x, ""), ["brandName", "seriesName", "class1Name", "class2Name"])))
            post_item["classes"] = result
        else:
            # not a QA post
            post_item["classes"] = ""
            # praise
        logger.info(post_item)
        yield post_item

        # if rid:
        #     praise_url = useful_url.format(tid=tid, rids=rid, t=time.time() * 1000)
        #     yield Request(praise_url, callback=self.parse_praise, headers={"Referer": post_item["url"]},
        #                   meta={"post_item": post_item})

    def parse_praise(self, response):
        logger.info('praise  url is {}'.format(response.url))
        post_item = response.meta["post_item"]
        body = response.body[15:]
        info = json.loads(body)["UsefulList"]
        if len(info) == 0:
            post_item["praise_num"] = 0
        else:
            post_item["praise_num"] = info[0]["UsefulCount"]
        logger.info(post_item)
        # dumper = CSVDumper("auto_qa_aodi.csv")
        # dumper.process_item(CSVLineItem(columns=post_item), None)

    def get_text(self, response):
        # kw_map = self.pool.apply(parse_kw, (response.body.decode("gbk", "ignore"),))
        kw_map = parse_kw(response.body.decode("gbk", "ignore"))
        page = etree.HTML(response.body.decode("gbk", "ignore"))

        if page.xpath('//div[@id="maxwrap-maintopic"]//div[@class="w740"]'):
            content = page.xpath('//div[@id="maxwrap-maintopic"]//div[@class="w740"]')[0]
        else:
            return ''
        for script in content.xpath('.//script'):
            script.text = ''

        for style in content.xpath('.//style'):
            style.text = ''

        fs = page.xpath('//span[@style="font-family: myfont;"]')
        for font in fs:
            if font.text.strip() in kw_map:
                font.text = kw_map[font.text.strip()]
        return content.xpath('normalize-space()').replace('%nbsp', ' ')

    @property
    def random_ip(self):
        return "201.{}.{}.{}".format(random.randrange(256), random.randrange(256), random.randrange(256))