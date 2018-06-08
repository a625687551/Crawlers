# -*- coding: utf-8 -*-

import time
import logging

from scrapy import Spider
from scrapy import Request

from CompanyCrawler.items import HousepriceItem

logger = logging.getLogger(__file__)
logger.setLevel(logging.INFO)

base_url = "http://esf.sjz.fang.com"
detail_tem = "http://{}.fang.com/xiangqing/"
area_list = [
    "/housing/357__0_0_0_0_1_0_0_0/",
    # "/housing/359__0_0_0_0_1_0_0_0/",
    # "/housing/358__0_0_0_0_1_0_0_0/",
    # "/housing/360__0_0_0_0_1_0_0_0/",
    # "/housing/361__0_0_0_0_1_0_0_0/",
    # "/housing/628__0_0_0_0_1_0_0_0/",
    # "/housing/629__0_0_0_0_1_0_0_0/",
    # "/housing/630__0_0_0_0_1_0_0_0/",
    # "/housing/632__0_0_0_0_1_0_0_0/",
    # "/housing/10114__0_0_0_0_1_0_0_0/"
]


class Fangtianxia(Spider):
    name = "fangtianxia"

    def start_requests(self):
        for area in area_list:
            list_url = base_url + area
            yield Request(list_url, callback=self.parse_list, meta={"area": area})

    def parse_list(self, response):
        content = response.xpath('//div[@class="houseList"]/div[@class="list rel"]/dl')
        for single in content:
            detail_url = single.xpath('./dt/a/@href').re_first("http://(.*?).fang.com/")
            detail_url = detail_tem.format(detail_url)
            yield Request(detail_url, callback=self.parse_detail)

        # next page
        if response.xpath('//a[@id="PageControl1_hlk_next"]/@href'):
            next_url = response.xpath('//a[@id="PageControl1_hlk_next"]/@href').extract_first()
            yield Request(next_url, callback=self.parse_list)

    def parse_detail(self, response):
        content = response.xpath('//div[@class="con clearfix"]')
        from IPython import embed
        embed()
        info_item = HousepriceItem({
            "city_name": u"石家庄",
            "house_name": content.xpath('//a[@class="tt"]/text()').extract_first(),
            "house_url": response.url,
            "house_address": content.xpath(u'.//strong[contains(./text(), "地址")]/../text()').extract_first(),
            "house_area": content.xpath(u'.//strong[contains(./text(), "所属区域")]/../text()').extract_first(),
            "house_price": content.xpath(u'.//div[@class="box detaiLtop mt20 clearfix"]//span[@class="red"]/text()').extract_first(),
            "post_code": content.xpath(u'.//strong[contains(./text(), "邮")]/../text()').extract_first(),
            "cycle_area": content.xpath(u'.//strong[contains(./text(), "环线位置")]/../text()').extract_first(),
            "property_right": content.xpath(u'.//strong[contains(./text(), "产权")]/../text()').extract_first(),
            "category": content.xpath(u'.//strong[contains(./text(), "类别")]/../text()').extract_first(),
            "house_year": content.xpath(u'.//strong[contains(./text(), "年代")]/../text()').extract_first(),
            "house_structure": content.xpath(u'.//strong[contains(./text(), "结构")]/../span/@title').extract_first(),
            "house_type": content.xpath(u'.//strong[contains(./text(), "类型")]/../text()').extract_first(),
            "house_num": content.xpath(u'.//strong[contains(./text(), "房屋总数")]/../text()').extract_first(),
            "building_num": content.xpath(u'.//strong[contains(./text(), "楼栋总数")]/../text()').extract_first(),
            "property_company": content.xpath(u'.//strong[contains(./text(), "物业公司")]/../text()').extract_first(),
            "green_rate": content.xpath(u'.//strong[contains(./text(), "绿")]/../text()').extract_first(),
            "volume_rate": content.xpath(u'.//strong[contains(./text(), "容")]/../text()').extract_first(),
            "property_cellphone": content.xpath(u'.//strong[contains(./text(), "物业办公")]/../text()').extract_first(),
            "property_cost": content.xpath(u'.//strong[contains(./text(), "物 业 费")]/../text()').extract_first(),
            "support_facility": content.xpath(u'normalize-space(.//div[contains(./div/h3/text(),"配套")]//dl)').extract_first(),
            "bad_thing": content.xpath(u'normalize-space(.//div[contains(./div/h3/text(),"嫌恶设施")]//dl)').extract_first(),
            "traffic_condition": content.xpath(u'normalize-space(.//div[contains(./div/h3/text(),"交通状况")]//dl)').extract_first(),
            "surround_info": content.xpath(u'normalize-space(.//div[contains(./div/h3/text(),"周边信息")]//dl)').extract_first(),
        })
        logger.info(info_item)
        yield info_item

