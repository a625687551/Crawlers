# -*- coding: utf-8 -*-

import logging
import sys

from lxml import etree
from scrapy import Spider
from scrapy.http import Request
from NormalCrawler.NormalCrawler.items import TiebaItem

date_format = '%Y-%m-%d %H:%M:%S'
logger = logging.getLogger(__name__)
reload(sys)
sys.setdefaultencoding('utf-8')


class BaiduTiebaSpider(Spider):
    name = "tieba_com"  # 百度贴吧
    author_url = "http://tieba.baidu.com/home/main?un={author_name}&fr=home"
    custom_settings = {
        "DOWNLOAD_DELAY": 0.2,
        "DEFAULT_REQUEST_HEADERS": {
            "Accept-Encoding": "gzip, deflate, sdch",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
        },
    }

    def start_requests(self):
        with open("tieba_urls.txt", "r") as f:
            for x in f.readlines():
                x = x.strip()
                if not x:
                    continue
                entry_id, url = map(lambda x: x.strip(), x.split(",", 1))
                # logger.info(u'will crawl url {} {}'.format(entry_id, url))
                yield Request(url, callback=self.parse_list, priority=5, meta={"entry_id": entry_id})

    def parse_list(self, response):
        html = etree.HTML(response.body.replace("<!--", "").replace("-->", ""))
        tieba_item = TiebaItem()
        tieba_item["tieba_url"] = response.url
        tieba_item["post_num"] = html.xpath('//span[@class]/span[@class="card_infoNum"]/text()')[0]
        logger.info(tieba_item)
        yield tieba_item




