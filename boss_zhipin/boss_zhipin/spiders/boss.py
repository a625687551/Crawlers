# coding:utf-8
import logging
import random
import json

from scrapy import Spider
from scrapy import Request
from urllib.parse import quote_plus
from lxml import etree

from boss_zhipin.items import BossItem

logger = logging.getLogger(__file__)
logger.setLevel(logging.INFO)
date_format = '%Y-%m-%d %H:%M:%S'


city_ids = {101010100: u"北京"}
key_words = ["数据分析"]
# list_url_tem = "https://www.zhipin.com/c{cid}/h_{cid2}/?query={kw}&page={pg}"
list_url_tem = "https://www.zhipin.com/mobile/jobs.json?page={pg}&city={cid}&query={kw}"


class ZhiPin(Spider):
    name = "zhipin"
    # custom_settings = {
    #     'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 '
    #                   '(KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1',
    # }

    def start_requests(self):
        for kw in key_words:
            for cid, name in city_ids.items():
                url = list_url_tem.format(kw=quote_plus(kw), cid=cid, pg=1)
                logger.info("will crawl url {}".format(url))
                yield Request(url=url, callback=self.parse_list, priority=6,
                              meta={"city": name, "kw": kw, "cid": cid}, headers={"X-Forward-For": random_ip()})

    def parse_list(self, response):
        logger.info("job list url {}".format(response.url))
        kw = response.meta["kw"]
        cid = response.meta["cid"]
        city = response.meta["city"]

        source = json.loads(response.body)
        # from IPython import embed
        # embed()
        content = etree.HTML(source["html"])
        pg = source["page"]
        for cell in content.xpath('//li[@class="item"]'):
            detail_url = response.urljoin(cell.xpath('./a/@href')[0])
            logger.info("will crawl detail {}".format(detail_url))
            yield Request(url=detail_url, callback=self.parse_detail, priority=1,
                          meta=response.meta, headers={"X-Forward-For": random_ip()})

        if pg < 10:
            pg = pg + 1
            next_url = list_url_tem.format(kw=quote_plus(kw), cid=cid, pg=pg)
            logger.info("will crawl url {}".format(next_url))
            yield Request(url=next_url, callback=self.parse_list, priority=6,
                          meta={"city": city, "kw": kw, "cid": cid}, headers={"X-Forward-For": random_ip()})

    def parse_detail(self, response):
        logger.info("job detail url {}".format(response.url))
        # from IPython import embed
        # embed()
        post_item = BossItem({
            "city": response.meta["city"],
            "job_name": response.xpath('//div[@class="job-banner"]/div[@class="name"]/text()').extract_first(),
            "job_url": response.url,
            "publish_time": response.xpath('//script[@type="application/ld+json"]').re_first(
                "\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}"),
            "company_name": response.xpath('//a[@class="job-company"]/div[@class="info-primary"]/div[@class="name"]/text()').extract_first(),
            "badge": response.xpath('//span[@class="salary"]/text()').extract_first(),
            "job_exp": response.xpath('//div[@class="job-banner"]/p/text()').extract()[1],
            "job_edu": response.xpath('//div[@class="job-banner"]/p/text()').extract()[2],
            "job_sec": response.xpath('normalize-space(//div[@class="job-sec"]/div[@class="text"])').extract_first(),
            "job_tags": response.xpath('//div[@class="job-tags"]/span[not(contains(@class, "time"))]/text()').extract(),
            "job_publisher_name": response.xpath('//div[@class="job-author"]//div[@class="name"]/text()').extract_first(),
            "job_publisher_post": response.xpath('//div[@class="job-author"]//p[@class="gray"]/text()').extract()[1],
        })
        logger.info(u"crawled {}".format(post_item))
        yield post_item


def random_ip():
    return "201.{}.{}.{}".format(random.randrange(256), random.randrange(256), random.randrange(256))