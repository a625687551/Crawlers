#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
# import uuid
import logging
import datetime
import multiprocessing

from lxml import etree
from scrapy import Spider
from scrapy import Request

# from pipelines.raw_data import RawDataItem
from extract.parser import parse_kw
from test.items import PostItem, UserItem
from utils import get_ip_str

logger = logging.getLogger(__file__)
logger.setLevel(logging.INFO)
date_format = '%Y-%m-%d %H:%M:%S'
prj_dir = os.path.dirname(os.path.relpath(__file__))



class AutohomeSpider(Spider):
    name = 'autohome'
    custom_settings = {
            'DOWNLOAD_DELAY': 3,
            'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
            }
    userinfo_api = 'http://i.autohome.com.cn/ajax/home/GetUserInfo?userid={}&r=&_='

    def start_requests(self):
        self.pool = multiprocessing.Pool(processes=1, maxtasksperchild=10)  # 1个进程，10次销毁一次
        # txt_path = os.path.join(tmp_dir, 'autohome.txt')
        # with open(txt_path, 'r') as f:
        #     urls = f.read()
        # urls = [url.split(',') for url in urls.split('\n') if url]
        # my_ip = get_ip_str()
        # idx = ip_list.index(my_ip)
        # tup = int(len(urls) / len(ip_list)) + 1
        # ret_urls = urls[tup*idx:tup*(idx+1)]
        # for entry_id, url in ret_urls:
        #     url = url + '?orderby=dateline'
        #     yield Request(
        #             url, callback=self.parse_list,
        #             meta={'entry_id': entry_id, 'deep': 1})
        # test code
        entry_id, url = 29242, 'http://club.autohome.com.cn/bbs/forum-c-148-1.html'
        url = url + '?orderby=dateline'
        yield Request(
            url, callback=self.parse_list,
            meta={'entry_id': entry_id, 'deep': 1})

    def parse_list(self, response):
        entry_id = response.meta['entry_id']
        lines = response.xpath('//div[@id="subcontent"]/dl[@class="list_dl"]')
        for line in lines:
            post_time = line.xpath('.//span[@class="tdate"]/text()').extract_first()
            if self.is_out(post_time):
                continue
            item = PostItem()
            item['entry_id'] = entry_id
            item['title'] = line.xpath('normalize-space(.//a[@class="a_topic"])').extract_first()
            path = line.xpath('.//a[@class="a_topic"]/@href').extract_first()
            item['url'] = response.urljoin(path)
            author_url = line.xpath('.//a[@class="linkblack"]/@href').extract_first()
            item['author_id'] = author_url.split('/')[-1]
            item['author_name'] = line.xpath('.//a[@class="linkblack"]/text()').extract_first()
            yield Request(
                    item['url'], callback=self.parse_detail,
                    meta={
                        'entry_id': entry_id, 'item': item, 'parent_url': item['url']
                        }
                    )
            yield Request(
                    author_url, callback=self.parse_author,
                    meta={
                        'entry_id': entry_id,
                        'author_id': item['author_id'],
                        'author_name': item['author_name']
                        })

        deep = response.meta['deep']
        if deep > 3:
            return
        deep += 1
        next_path = response.xpath('//a[@class="afpage"]/@href').extract_first()
        next_url = response.urljoin(next_path)
        yield Request(
                next_url, callback=self.parse_list,
                meta={'entry_id': entry_id, 'deep': deep}
                )

    def parse_detail(self, response):
        entry_id = response.meta['entry_id']
        item = response.meta.get('item', None)
        parent_url = response.meta['parent_url']
        if item:
            firstline = response.xpath('//div[@id="maxwrap-maintopic"]/div[@class="clearfix contstxt outer-section"]')
            item['data_type'] = 'first'
            item['text'] = self.get_text(response)
            item['img_url'] = firstline.xpath('.//div[@class="conttxt"]//img/@src').extract()
            item['read_num'] = response.xpath('//font[@id="x-views"]/text()').extract_first()
            item['comment_num'] = response.xpath('//font[@id="x-replys"]/text()').extract_first()
            item['post_time'] = firstline.xpath('.//span[@xname="date"]/text()').extract_first()
            logger.info(
                    'crawled post title: %s, post_time:%s, comment_num: %s, read_num: %s, \n url: %s',
                    item['title'], item['post_time'], item['comment_num'], item['read_num'], item['url'])
            post_item = item
            yield item
        lines = response.xpath('//div[@id="maxwrap-reply"]/div[@class="clearfix contstxt outer-section"]')
        for line in lines:
            item = PostItem()
            item['entry_id'] = entry_id
            author_url = line.xpath('.//li[@class="txtcenter fw"]/a[1]/@href').extract_first()
            author_id = re.findall('autohome.com.cn/(\\d+)', author_url)[0]
            author_name = line.xpath('.//li[@class="txtcenter fw"]/a[1]/@title').extract_first()
            item['author_id'] = author_id
            item['author_name'] = author_name
            item['data_type'] = 'comment'
            num = line.xpath('.//button[@class="rightbutlz"]/text()').extract_first()
            item['url'] = parent_url + '#' + num
            if line.xpath('.//div[@class="yy_reply_cont"]'):
                text = line.xpath('normalize-space(.//div[@class="yy_reply_cont"])').extract_first()
            else:
                text = line.xpath('normalize-space(.//div[@class="w740"])').extract_first()
            item['text'] = text
            item['post_time'] = line.xpath('.//span[@xname="date"]/text()').extract_first()
            item['parent_url'] = parent_url
            logger.info('crawled comment: %s %s %s', item['text'], item['post_time'], item['url'])
            comment_item = item
            yield item
            yield Request(
                    author_url, callback=self.parse_author,
                    meta={
                        'entry_id': entry_id,
                        'author_id': author_id,
                        'author_name': author_name
                        }
                    )
        ttitem = ' '.join(post_item['text'] + comment_item['text'])
        logger.info('TEST ``````````````%s', ttitem)
        # yield RawDataItem({
        #     "url": response.url,
        #     "content": self._unicode_body(response),
        # })
        next_path = response.xpath('//a[@class="afpage"]/@href').extract_first()
        if not next_path:
            return
        next_url = response.urljoin(next_path)
        yield Request(
                next_url, callback=self.parse_detail,
                meta={
                    'entry_id': entry_id,
                    'parent_url': parent_url
                    }
                )

    def parse_author(self, response):
        item = UserItem()
        item['entry_id'] = response.meta['entry_id']
        item['author_id'] = response.meta['author_id']
        item['author_name'] = response.meta['author_name']
        item['avatar'] = response.xpath('//div[@class="userHead"]/a/img/@src').extract_first()
        item['home_page'] = response.url
        item['follow_num'] = response.xpath('//div[@class="user-lv"]/a[@class="state-mes"][1]/span/text()').extract_first()
        item['fans_num'] = response.xpath('//div[@class="user-lv"]/a[@class="state-mes"][2]/span/text()').extract_first()
        try:
            place = response.xpath('//a[@class="state-pos"]/text()').extract_first().strip()
            item['province'], item['city'] = place.split(' ')
        except:
            pass

        userinfo_api = self.userinfo_api.format(item['author_id'])
        headers = {'Referer': response.url}
        yield Request(
                userinfo_api, callback=self.parse_userinfo,
                headers=headers, meta={'item': item}
                )

    def parse_userinfo(self, response):
        item = response.meta['item']
        item['post_num'] = re.findall('"TopicCount":(\\d+),', response.body)[0]
        logger.info('crawled author: %s %s', item['author_name'], item['home_page'])
        yield item

    def is_out(self, post_time):
        now = datetime.datetime.now()
        post_time = datetime.datetime.strptime(post_time, '%Y-%m-%d')
        if (now - post_time).days > 2:
            return True
        return False

    def get_text(self, response):
        kw_map = self.pool.apply(parse_kw, (response.body,))
        # kw_map = parse_kw(response.body)
        page = etree.HTML(response.body)
        try:
            content = page.xpath('//div[@id="maxwrap-maintopic"]//div[@class="w740"]')[0]
        except:
            # uid1 = uuid.uuid1()
            # filepath = os.path.join('/home/dingyong/zxp/log/autohome_error', uid1.hex + '.html')
            # with open(filepath, 'w') as f:
            #     f.write(response.body)
            # logger.warning('Parse content error! url: filepath: %s', response.url, filepath)
            pass

        for script in content.xpath('.//script'):
            script.text = ''

        for style in content.xpath('.//style'):
            style.text = ''

        for span in content.xpath('.//span[contains(@class, "hs_kw")]'):
            num = re.findall('hs_kw(\d+)_', span.attrib['class'])[0]
            span.text = kw_map[num]
        return content.xpath('normalize-space()').replace('%nbsp', '')

    def closed(self, reason):
        if hasattr(self, "pool"):
            self.pool.close()

    @staticmethod
    def _unicode_body(response):
        try:
            return response.body_as_unicode()
        except:
            try:
                return response.body.decode(response.encoding, "ignore")
            except:
                return response.body.decode("utf-8", "ignore")
