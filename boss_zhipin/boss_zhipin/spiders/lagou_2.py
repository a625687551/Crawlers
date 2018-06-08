# coding:utf-8
import logging
import random
import json

from scrapy import Spider
from scrapy import Request
from scrapy import FormRequest
from urllib.parse import quote_plus
from lxml import etree

from boss_zhipin.items import BossItem

logger = logging.getLogger(__file__)
logger.setLevel(logging.INFO)
date_format = '%Y-%m-%d %H:%M:%S'

key_words = ["数据分析", "数据挖掘", "数据建模", "机器学习"]

headers = {
    "Host": "www.lagou.com",
    "Connection": "Keep-alive",
    "Origin": "https://www.lagou.com",
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Referer": "https://www.lagou.com/jobs/list_%E6%95%B0%E6%8D%AE%E6%8C%96%E6%8E%98",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome Safari/537.36",
    }


class LaGou(Spider):
    name = "lagou_2"
    custom_settings = {
        "DOWNLOAD_DELAY": 3,
        "COOKIES_ENABLED": False,
        "DOWNLOAD_TIMEOUT": 30,
        "DOWNLOADER_MIDDLEWARES": {
            'boss_zhipin.middlewares.RandomProxyMiddleware': 100,
        },
    }
    list_url_tem = "https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false"
    detail_url = "https://www.lagou.com/jobs/{}.html"
    refer = "https://www.lagou.com/jobs/list_{}?labelWords=&fromSearch=true&suginput="

    def start_requests(self):
        for kw in key_words:
            pg = 1
            post_body = {
                'first': "true",
                'pn': str(pg),
                'kd': kw
            }
            logger.info("will crawl url {}".format(self.list_url_tem))
            yield FormRequest(url=self.list_url_tem, callback=self.parse_list, priority=6, formdata=post_body,
                              meta={"kw": kw, "pg": pg}, headers=headers)

    def parse_list(self, response):
        logger.info("job list url {}".format(response.url))
        kw = response.meta["kw"]
        pg = response.meta["pg"]

        content = json.loads(response.body)

        for cell in content['content']["positionResult"]["result"]:
            post_item = BossItem()
            post_item["city"] = cell["city"]
            post_item["job_name"] = cell["positionName"]
            post_item["job_url"] = self.detail_url.format(cell["positionId"])
            post_item["publish_time"] = cell["createTime"]
            post_item["company_name"] = cell["companyFullName"]
            post_item["company_industry"] = cell["industryField"]
            post_item["company_stage"] = cell["financeStage"]
            post_item["job_welfare"] = cell["positionAdvantage"]
            post_item["job_salary"] = cell["salary"]
            post_item["job_exp"] = cell["workYear"]
            post_item["job_edu"] = cell["education"]
            post_item["job_sec"] = cell["education"]
            post_item["job_tags"] = cell["positionLables"]

            yield post_item

        if pg < 30:
            pg = pg + 1
            post_body = {
                'first': "false",
                'pn': str(pg),
                'kd': kw
            }
            logger.info("will crawl url {}".format(self.list_url_tem))
            yield FormRequest(url=self.list_url_tem, callback=self.parse_list, priority=6, formdata=post_body,
                              meta={"kw": kw, "pg": pg}, headers=headers)
