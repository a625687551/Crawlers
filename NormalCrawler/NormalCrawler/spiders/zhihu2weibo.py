# coding:utf-8

import os
import sys
import json
import random
import logging

from scrapy import Spider
from scrapy import Request
from test.items import Zhihu2Weibo

logger = logging.getLogger(__file__)
logger.setLevel(logging.INFO)
date_format = '%Y-%m-%d %H:%M:%S'
reload(sys)
sys.setdefaultencoding('utf8')


class ZhihuSpdier(Spider):
    name = 'zhihu2weibo'

    custom_settings = {
        "DOWNLOAD_DELAY": 1,
        "DEFAULT_REQUEST_HEADERS": {
            'Accept-Encoding': 'gzip, deflate',
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 5.1.1; 2014812 Build/LMY49J)',
            'Connection': 'Keep-Alive',
            'Host': 'api.zhihu.com',
            'x-api-version': '3.0.54',
            'Authorization': "oauth 8d5227e0aaaa4797a763ac64e0c3b8",
            'x-app-za': 'OS=Android&Release=5.1.1&Model=2014812&VersionName=4.56.1&VersionCode=521&'
                        'Width=720&Height=1280&Installer=%E8%B1%8C%E8%B1%86%E8%8D%9A&WebView=47.0.2526.100',
        },
    }

    user_url = 'https://api.zhihu.com/people/{uid}'  # 8f9ea27708c374cc1d6c447d0bf277ab 知乎ID都是经过hash

    def start_requests(self):
        with open("zhihu_kol.txt", "r") as f:
            users = f.readlines()
        for index, user_id in enumerate(users):
            user_id = user_id.strip()
            logger.info(u'will crawl order {} kol name {} id {}'.format(index, "XXXx", user_id))

            yield Request(self.user_url.format(uid=user_id), priority=10, callback=self.parse_kol_info,
                          meta={'page': 0, "user_id": user_id}, headers={'X-Forwarded-For': self.random_ip()})

    def parse_kol_info(self, response):
        content = json.loads(response.body)

        item = Zhihu2Weibo({
            "user_id": response.meta["user_id"],
            "weibo_url": content.get("sina_weibo_url", ""),
            "weibo_name": content.get("sina_weibo_name", ""),
        })
        yield item
        logger.info(item)

    @staticmethod
    def random_ip():
        return "{}.{}.{}.{}".format(random.randrange(210, 250), random.randrange(256), random.randrange(256),
                                    random.randrange(256))