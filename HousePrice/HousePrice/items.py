# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class HousepriceItem(scrapy.Item):
    house_name = Field()  # 小区名称
    house_url = Field()  # 小区网址
    house_address = Field()  # 小区地址
    house_area = Field()  # 小区所属区域
    house_price = Field()  # 房价
    post_code = Field()  # 邮编
    cycle_area = Field()  # 环线位置
    property_right = Field()  # 产权
    category = Field()  # 小区类型：住宅、商品
    house_year = Field()  # 建筑年代
    house_structure = Field()  # 建筑结构
    house_type = Field()  # 建筑类型：板楼
    house_num = Field()  # 房屋总数
    building_num = Field()  # 楼栋数
    property_company = Field()  # 物业公司
    green_rate = Field()  # 绿化率
    volume_rate = Field()  # 容积率
    property_cellphone = Field()  # 物业电话
    property_cost = Field()  # 物业费用
    support_facility = Field()  # 配套设施
    bad_thing = Field()  # 不好的事情
    traffic_condition = Field()  # 交通情况
    surround_info = Field()  # 周边信息
