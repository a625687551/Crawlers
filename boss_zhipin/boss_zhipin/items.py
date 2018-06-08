# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item
from scrapy import Field


class BossItem(Item):
    city = Field()  # 城市
    job_name = Field()  # 工作名称
    job_url = Field()  # 工作网址
    publish_time = Field()  # 发布日期
    company_name = Field()  # 公司名字
    company_industry = Field()  # 公司领域、行业
    company_stage = Field()  # 公司融资阶段
    job_welfare = Field()  # 公司福利
    job_salary = Field()  # 薪酬
    job_exp = Field()  # 工作经验要求
    job_edu = Field()  # 学历要求
    job_sec = Field()  # 工作描述
    job_tags = Field()  # 工作标签（关键词）
    job_publisher_name = Field()  # 发布人姓名
    job_publisher_post = Field()  # 发布人职位


class JobItem(Item):
    city = Field()  # 城市
    job_name = Field()  # 工作名称
    job_url = Field()  # 工作网址
    publish_time = Field()  # 发布日期
    company_name = Field()  # 公司名字
    badge = Field()  # 薪酬
    job_exp = Field()  # 工作经验要求
    job_edu = Field()  # 学历要求
    job_sec = Field()  # 工作描述
    job_tags = Field()  # 工作标签（关键词）
    job_publisher_name = Field()  # 发布人姓名
    job_publisher_post = Field()  # 发布人职位
