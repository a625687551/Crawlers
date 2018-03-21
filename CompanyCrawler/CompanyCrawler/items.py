# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class CompanycrawlerItem(scrapy.Item):
        # define the fields for your item here like:
        # 企业名字
        name = scrapy.Field()
        # 企业电话
        phone = scrapy.Field()
        # 企业邮箱
        mail = scrapy.Field()
        # 企业网页地址
        net_addr = scrapy.Field()
        # 企业地址
        addr = scrapy.Field()
        # 企业描述
        desc = scrapy.Field()
        # 法人
        faren = scrapy.Field()
        # 拥有的公司
        owner_company = scrapy.Field()
        # 注册资本
        register_money = scrapy.Field()
        # 注册时间
        register_time = scrapy.Field()
        # 公司状态
        company_state = scrapy.Field()
        # 工商注册代码
        registration_num = scrapy.Field()
        # 组织机构代码
        organization_num = scrapy.Field()
        # 统一信用代码
        credit_num = scrapy.Field()
        # 公司类型
        company_type = scrapy.Field()
        # 纳税人识别号
        taxpayer_num = scrapy.Field()
        # 行业
        ndustry = scrapy.Field()
        # 营业期限
        bussiness_time = scrapy.Field()
        # 核准时间
        check_time = scrapy.Field()
        # 登记机关
        register_office = scrapy.Field()
        # 英文名字
        company_eng = scrapy.Field()
        # 注册地址
        register_addr = scrapy.Field()
        # 经营范围
        manage_orange = scrapy.Field()


class HousepriceItem(scrapy.Item):
    city_name = Field()   # 城市名字
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