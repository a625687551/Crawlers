# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item
from scrapy import Field


class NormalcrawlerItem(scrapy.Item):
    pass


class UserItem(Item):
    author_id = Field()
    author_name = Field()
    avatar = Field()  # 头像
    home_page = Field()  # 个人主页
    fans_num = Field()
    follow_num = Field()
    post_num = Field()
    comment_num = Field()
    like_num = Field()
    photo_num = Field()
    gender = Field()  # 性别  m：男、f：女、n：未知
    birthday = Field()
    description = Field()  # 简介
    is_verified = Field()  # 是否认证
    verified_reason = Field()  # 认证信息
    current_state = Field()  # 当前状态 (备孕XX/宝宝X岁X个月)
    level = Field()  # 等级/level/皇冠
    exp = Field()  # 威望/经验
    register_time = Field()  # 注册时间
    profession = Field()  # 职业信息
    education = Field()  # 教育信息
    province = Field()  # 地域（省）
    city = Field()  # 地域（市）
    client = Field()  # 终端
    entry_id = Field()
    site_id = Field()
    site_name = Field()


class PostItem(Item):
    author_id = Field()
    author_name = Field()
    site_type = Field()  # 按照32服务器上bsppr数据库source表。微博：5，论坛：2，APP：15
    url = Field()
    title = Field()
    text = Field()
    img_url = Field()  # list
    video_url = Field()  # list
    read_num = Field()
    like_num = Field()
    comment_num = Field()
    repost_num = Field()  # 转发数
    collect_num = Field()  # 收藏数
    post_time = Field()  # 发布时间
    include_time = Field()  # 抓取时间
    parent_url = Field()  # 首楼url 用于关联分楼 一楼不写
    entry_id = Field()
    data_type = Field()
    site_id = Field()
    site_name = Field()


class TiebaItem(Item):
    # tieba_name = Field()  # 贴吧名字
    tieba_url = Field()  # 贴吧URL
    # category = Field()  # 分类
    # baidu_tag = Field()  # 百度标签
    # mem_num = Field()  # 关注数
    post_num = Field()  # 发帖数


class LiveItem(Item):
    author_id = Field()
    author_name = Field()
    site_id = Field()  # monitoring media id
    site_name = Field()  # monitoring media name
    url = Field()  # webpage link
    title = Field()  # title
    read_num = Field()  # article read number, video watch times ,live view number
    online_num = Field()  # online view number
    like_num = Field()  # praise number
    comment_num = Field()  # comment number
    post_time = Field()  # realise time or update time or start time
    include_time = Field()  # crawl time
    content_tags = Field()  # article(video, live) tags string
    video = Field()  # video url string
    image = Field()  # cover image string


class CompanyItem(Item):
    company_name = Field()
    url = Field()
    company_url = Field()
    company_phone = Field()
    company_email = Field()
    company_address = Field()
    company_description = Field()


class AnswerItem(Item):
    title = Field()
    url = Field()
    ask = Field()
    answer = Field()
    qa_class = Field()


class Zhihu2Weibo(Item):
    user_id = Field()
    weibo_url = Field()
    weibo_name = Field()


class BossItem(Item):
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

