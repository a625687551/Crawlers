# -*- coding: utf-8 -*-

import time
import logging

from scrapy import Spider
from scrapy import Request

from NormalCrawler.NormalCrawler.items import HousepriceItem

logger = logging.getLogger(__file__)
logger.setLevel(logging.INFO)

base_url = "http://esf.sjz.fang.com"
detail_tem = "http://{}.fang.com/xiangqing/"
area_list = [
    "/housing/357__0_0_0_0_1_0_0_0/"
    "/housing/359__0_0_0_0_1_0_0_0/"
    "/housing/358__0_0_0_0_1_0_0_0/"
    "/housing/360__0_0_0_0_1_0_0_0/"
    "/housing/361__0_0_0_0_1_0_0_0/"
    "/housing/628__0_0_0_0_1_0_0_0/"
    "/housing/629__0_0_0_0_1_0_0_0/"
    "/housing/630__0_0_0_0_1_0_0_0/"
    "/housing/632__0_0_0_0_1_0_0_0/"
    "/housing/10114__0_0_0_0_1_0_0_0/"
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

    def parse_detail(self, response):
        content = response.xpath('//div[@class="con clearfix"]')
        info_item = HousepriceItem({
            "city_name": u"石家庄",
            "house_name": content.xpath('//a[@class="tt"]/text()').extract_first,
            "house_url": response.url,
            "house_address": content.xpath('//dl[@class="clearfix mr30"]//strong[contains(./text(), u"地址")]/../text()').extract_first,
            "house_area": content.xpath('//dl[@class="clearfix mr30"]//strong[contains(./text(), u"所属区域")]/../text()').extract_first,
            "house_price": content.xpath('//div[@class="box detaiLtop mt20 clearfix"]//span[@class="red"]/text()').extract_first,
            "post_code": content.xpath('//dl[@class="clearfix mr30"]//strong[contains(./text(), u"邮")]/../text()').extract_first,
            "cycle_area": content.xpath('//dl[@class="clearfix mr30"]//strong[contains(./text(), u"环线位置")]/../text()').extract_first,
            "property_right": content.xpath('//dl[@class="clearfix mr30"]//strong[contains(./text(), u"产权")]/../text()').extract_first,
            "category": content.xpath('//dl[@class="clearfix mr30"]//strong[contains(./text(), u"类别")]/../text()').extract_first,
            "house_year": content.xpath('//dl[@class="clearfix mr30"]//strong[contains(./text(), u"年代")]/../text()').extract_first,
            "house_structure": content.xpath('//dl[@class="clearfix mr30"]//strong[contains(./text(), u"结构")]/../span/@title').extract_first,
            "house_type": content.xpath('//dl[@class="clearfix mr30"]//strong[contains(./text(), u"类型")]/../text()').extract_first,
            "house_num": content.xpath('//dl[@class="clearfix mr30"]//strong[contains(./text(), u"房屋总数")]/../text()').extract_first,
            "building_num": content.xpath('//dl[@class="clearfix mr30"]//strong[contains(./text(), u"楼栋总数")]/../text()').extract_first,
            "property_company": content.xpath('//dl[@class="clearfix mr30"]//strong[contains(./text(), "u物业公司")]/../text()').extract_first,
            "green_rate": content.xpath('//dl[@class="clearfix mr30"]//strong[contains(./text(), u"绿")]/../text()').extract_first,
            "volume_rate": content.xpath('//dl[@class="clearfix mr30"]//strong[contains(./text(), u"容")]/../text()').extract_first,
            "property_cellphone": content.xpath('//dl[@class="clearfix mr30"]//strong[contains(./text(), u"物业办公")]/../text()').extract_first,
            "property_cost": content.xpath('//dl[@class="clearfix mr30"]//strong[contains(./text(), u"物 业 费")]/../text()').extract_first,
            "support_facility": content.xpath('normalize-space(//div[contains(./div/h3/text(),u"配套")]//dl)').extract_first,
            "bad_thing": content.xpath('normalize-space(//div[contains(./div/h3/text(),u"嫌恶设施")]//dl)').extract_first,
            "traffic_condition": content.xpath('normalize-space(//div[contains(./div/h3/text(),u"交通状况")]//dl)').extract_first,
            "surround_info": content.xpath('normalize-space(//div[contains(./div/h3/text(),u"周边信息")]//dl)').extract_first,
        })
        logger.info(info_item)
        yield info_item

