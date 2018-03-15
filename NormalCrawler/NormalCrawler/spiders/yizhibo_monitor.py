# -*- coding: utf-8 -*-

"""这里主要解决监控针对的主播现在直播中的观看人数"""

import time
import js2py
import logging
import re
import sys
import time

from scrapy import Request
from scrapy import Spider

import dateformatting
from test.items import LiveItem

logger = logging.getLogger(__file__)
logger.setLevel(logging.INFO)
date_format = '%Y-%m-%d %H:%M:%S'
reload(sys)
sys.setdefaultencoding('utf8')


class YizhiboMonitor(Spider):
    name = "yizhibomonitor"
    url = "https://www.yizhibo.com/member/personel/user_works?memberid={uid}"
    custom_settings = {
                "DOWNLOAD_DELAY": 3,
                "DEFAULT_REQUEST_HEADERS": {
                    'Accept-Encoding': 'gzip, deflate, sdch, br',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                  'Chrome/58.0.3029.110 Safari/537.36',
                },
            }

    def start_requests(self):
        for i in xrange(20):
            users = self.settings.get("UIDS")
            if users:
                users = users.split(",")
            else:
                users = ["32655740", "275536549", "470266", "145904104", "4685800", "197096389", "274163032", "133470596"]
                # users = ["121488994"]
            for uid in users:
                logger.info(uid)
                yield Request(url=self.url.format(uid=uid), callback=self.parse_view_count, meta={"uid": uid})
            time.sleep(60)

    def parse_view_count(self, response):
        logger.info("live list {}".format(response.url))
        info = response.xpath('//ul[@class="index_all index_all_all cf"]/li[@class="index_all_common index_zb"]')
        if len(info) == 0:
            logger.info("no living now !!!----------------------------")
            return
        else:
            title = info.xpath('normalize-space(.//div[contains(@class, "index_intro")]/text())').extract_first()
            live_url = response.urljoin(info.xpath('.//a/@href').extract_first())
            yield Request(url=live_url, callback=self.parse_live_detail)

    def parse_live_detail(self, response):
        logger.info("live url {}".format(response.url))
        info = re.findall("window.(anchor = .*?);", response.body, re.S)[0]
        post_info = js2py.eval_js(info)

        post_item = LiveItem()
        post_item["author_id"] = post_info["memberid"]
        post_item["author_name"] = post_info["nickname"]
        post_item["url"] = response.url
        post_item["title"] = response.xpath("//h1/text()").extract_first()
        post_item["site_id"] = 1223
        post_item["site_name"] = "一直播"
        # post_item["read_num"] = post_info["online"]
        post_item["online_num"] = post_info["online"]  # 文章阅读数 视频观看数 live参加数
        post_item["like_num"] = response.xpath('//div[@class="hide"]').re_first(u"共有(\d+)条点赞")  # 点赞数
        post_item["comment_num"] = response.xpath('//div[@class="hide"]').re_first(u"共有(\d+)条评论")  # 评论数
        post_item["post_time"] = dateformatting.parse(post_info["starttime"]).strftime(date_format)  # 发布时间
        post_item["include_time"] = self.crawled_time  # 抓取时间
        post_item["content_tags"] = response.xpath('//div[@class="hide"]').re_first(u"认证类型:(.*?)。")
        post_item["video"] = post_info["play_url"]
        post_item["image"] = post_info["covers"]
        yield post_item
        # logger.info(post_item)

        logger.info(u"{} live view people {}".format(post_item["author_name"], post_item["online_num"]))

    @property
    def crawled_time(self):
        return time.strftime(date_format, time.localtime())

    @property
    def timeout_date(self):
        return dateformatting.parse(self.settings.get("AFTER_DATE", u"3天前"))