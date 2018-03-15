# coding:utf-8
import logging
import sys
import json

from scrapy import Spider
from scrapy import Request
from urllib.parse import quote_plus
from lxml import etree

from NormalCrawler.NormalCrawler.items import BossItem

logger = logging.getLogger(__file__)
logger.setLevel(logging.INFO)
date_format = '%Y-%m-%d %H:%M:%S'
reload(sys)
sys.setdefaultencoding('utf8')

city_ids = {101010100: u"北京"}
key_words = ["数据分析"]
# list_url_tem = "https://www.zhipin.com/c{cid}/h_{cid2}/?query={kw}&page={pg}"
list_url_tem = "https://www.zhipin.com/mobile/jobs.json?page={pg}&city={cid}&query={kw}"


class ZhiPin(Spider):
    name = "zhipin"
    custom_settings = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 '
                      '(KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1',
    }

    def start_requests(self):
        for kw in key_words:
            for cid in city_ids.iterkeys():
                url = list_url_tem.format(kw=quote_plus(kw), cid=cid, pg=1)
                logger.info("will crawl url {}".format(url))
                yield Request(url=url, callback=self.parse_list, priority=6,
                              meta={"city": city_ids[cid], "kw": kw, "pg": 1, "cid": cid})

    def parse_list(self, response):
        logger.info("job list url {}".format(response.url))
        kw = response.meta["kw"]
        cid = response.meta["cid"]
        source = json.loads(response.body)
        content = etree.HTML(source["html"])
        pg = source["page"]
        # content = response.xpath('//div[@class="job-list"]/ul/li')
        from IPython import embed
        embed()
        for cell in content:
            detail_url = response.urljoin(cell.xpath('.//h3[@class="name"]/a/@href').extract_first())
            logger.info("will crawl detail {}".format(detail_url))
            yield Request(url=detail_url, callback=self.parse_detail, priority=1, meta=response.meta)

        # if pg < 10:
        #     pg = pg + 1
        #     next_url = list_url_tem.format(kw=quote_plus(kw), cid=cid, cid2=cid, pg=pg)
        #     logger.info("will crawl url {}".format(next_url))
        #     yield Request(url=next_url, callback=self.parse_list, priority=6,
        #                   meta={"city": city_ids[cid], "kw": kw, "pg": pg, "cid": cid})

    def parse_detail(self, response):
        logger.info("job detail url {}".format(response.url))
        post_item = BossItem({
            "city": response.meta["city"],
            "job_name": response.xpath('//h1/text()').extract_first(),
            "job_url": response.url,
            "publish_time": response.xpath('//div[@class="job-author"]/span/text()').re_first("\d{4}-\d{2}-\d{2} \d{2}:\d{2}"),
            "company_name": response.xpath('//h3[@class="name"]/a/text()').extract_first(),
            "badge": response.xpath('//div[@class="job-primary detail-box"]//div[@class="name"]/span/text()').extract_first(),
            "job_exp": response.xpath('//div[@class="job-primary detail-box"]/div[@class="info-primary"]/p').re_first(u"</em>经验：(.*?)<em"),
            "job_edu": response.xpath('//div[@class="job-primary detail-box"]/div[@class="info-primary"]/p').re_first(u"</em>学历：(.*?)</p>"),
            "job_sec": response.xpath('normalize-space(//div[@class="job-sec"]/div[@class="text"])').extract_first(),
            "job_tags": response.xpath('//div[@class="info-primary"]/div[@class="job-tags"]/span/text()').extract(),
            "job_publisher_name": response.xpath('//h2/text()').extract_first(),
            "job_publisher_post": response.xpath('//div[@class="detail-op"]/p/text()').extract_first(),
        })
        logger.info(u"crawled {}".format(post_item["job_url"]))
        yield post_item
