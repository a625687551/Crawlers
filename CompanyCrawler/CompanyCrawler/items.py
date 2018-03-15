# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


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
