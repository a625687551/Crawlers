# coding:utf-8
import logging

from scrapy import Spider
from scrapy import Request
from NormalCrawler.NormalCrawler.items import AnswerItem

logger = logging.getLogger(__file__)
logger.setLevel(logging.INFO)
date_format = '%Y-%m-%d %H:%M:%S'


class Aikaqa(Spider):
    name = "aika_qa"
    start_url = "http://www.xcar.com.cn/bbs/forumdisplay.php?fid=1753"

    def start_requests(self):
        yield Request(self.start_url, callback=self.parse_list, meta={"page": 1})

    def parse_list(self, response):
        page = response.meta["page"]
        content = response.xpath('//div[@class="post-list"]//div[@class="plr20"]/dl')
        for sinle in content:
            url = response.urljoin(sinle.xpath('.//p[@class="thenomal"]/a/@href').extract_first())
            title = response.urljoin(sinle.xpath('.//p[@class="thenomal"]/a/text()').extract_first())
            logger.info(u"will crawl {}".format(title))
            yield Request(url, callback=self.parse_post, meta={"url": url, "title": title})

        if page < 36:
            page += 1
            next_page = response.urljoin(response.xpath('//a[@class="page_down"]/@href').extract_first())
            yield Request(next_page, callback=self.parse_list, meta={"page": page})

    def parse_post(self, response):
        post_item = AnswerItem({
            "title": response.meta["title"],
            "url": response.meta["url"],
            "ask": response.xpath('normalize-space(//div[contains(@id, "message")])').extract_first(),
            "answer": response.xpath('normalize-space(//div[@class="answer_info"])').extract_first(),
        })
        logger.info(u"crawled {}".format(post_item["title"]))
        yield post_item
