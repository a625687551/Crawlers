# !/usr/bin/env python
# -*- coding:utf-8 -*-

"""
汽车之家问答帖抓取程序
"""

import time
import random
import urlparse
import re
import os
import json
import time
import random
import urllib
import logging
import tempfile
import traceback

import psutil
import requests
from lxml import etree
from scrapy import Spider
from scrapy import Request
from scrapy import Spider

from fontTools.ttLib import TTFont
from fontTools.pens.basePen import BasePen
from reportlab.lib import colors
from reportlab.graphics import renderPM
from reportlab.graphics.shapes import Path
from reportlab.graphics.shapes import Group, Drawing, scale
from pipelines.csv_dumper import CSVDumper, CSVLineItem

TTF_PATTERN = re.compile(r"url\('([^']+?ttf)'\)")
ttf_file = tempfile.NamedTemporaryFile(suffix=".ttf")
png_file = tempfile.NamedTemporaryFile(suffix=".png")

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
date_format = '%Y-%m-%d %H:%M:%S'

useful_url = "https://zhidao.autohome.com.cn/ajax/GetUsefulInfo?tid={tid}&rids={rids}&_={t}"
class_url = "https://zhidao.autohome.com.cn/ajax/ZhidaoForClubTopicMerge?tid={tid}"


class AutohomeQa(Spider):
    name = "autohome_qa"

    custom_settings = {
        "DOWNLOAD_DELAY": 3,
        ""
        "DEFAULT_REQUEST_HEADERS": {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/57.0.2986.0 Safari/537.36',
        },
    }

    def start_requests(self):
        # with open("u1s.txt") as f:
        #     lines = f.readlines()
        # lines = [line.strip() for line in lines if line.strip()]
        # for url in lines:
        #     logger.info("Request list url:{}".format(url))
        #     yield Request(url, callback=self.parse_list, headers={"X-Forwarded-For": self.random_ip})
        # test
        url = "https://zhidao.autohome.com.cn/list/b33/s4-1.html"
        yield Request(url, callback=self.parse_list, headers={"X-Forwarded-For": self.random_ip})

    def parse_list(self, response):
        logger.info('list url is {}'.format(response.url))

        hrefs = response.xpath('//ul[@class="qa-list-con"]//a/@href').extract()
        for href in hrefs:
            href = re.sub("http:", "https:", href)
            logger.info('will crawl detail url is {}'.format(href))
            yield Request(href, callback=self.parse_detail, headers={"X-Forwarded-For": self.random_ip})
        next_page = response.xpath('//a[@class="page-item-next"]/@href').extract_first()
        if next_page:
            next_url = response.urljoin(next_page)
            logger.info("will crawl next page {}".format(next_url))
            yield Request(next_url, callback=self.parse_list, headers={"X-Forwarded-For": self.random_ip})

    def parse_detail(self, response):
        logger.info('detail url is {}'.format(response.url))

        post_item = {}
        post_item["title"] = response.xpath('//div[@id="consnav"]/span[last()]/text()').extract_first()
        # post_item["first_floor_content"] = response.xpath('normalize-space(//div[@class="conttxt"])').extract_first()
        post_item["first_floor_content"] = self.get_text(response)
        post_item["second_floor_content"] = response.xpath('normalize-space((//div[contains(@class, "x-reply")])[1])').extract_first()
        post_item["url"] = response.url
        tid = response.xpath('//div[contains(@name, "replyuseful")]/@data-tid').extract_first()
        rid = response.xpath('//div[contains(@name, "replyuseful")]/@data-rid').extract_first()

        # class
        cat_url = class_url.format(tid=tid)
        yield Request(cat_url, callback=self.parse_class, headers={"Referer": response.url},
                      meta={"post_item": post_item, "tid": tid, "rid": rid})

    def parse_class(self, response):
        logger.info('class url is {}'.format(response.url))
        post_item = response.meta["post_item"]
        tid = response.meta["tid"]
        rid = response.meta["rid"]

        data_list = re.findall(r"var qaextend = ({.*?});", response.body)
        if data_list:
            data = json.loads(data_list[0].decode("gbk"))
            # result = " > ".join(
            #     map(lambda x: data.get(x, "").strip(), ["brandName", "seriesName", "class1Name", "class2Name"]))
            result = " > ".join(
                filter(None, map(lambda x: data.get(x, ""), ["brandName", "seriesName", "class1Name", "class2Name"])))
            post_item["classes"] = result
        else:
            # not a QA post
            post_item["classes"] = ""
            # praise
        praise_url = useful_url.format(tid=tid, rids=rid, t=time.time() * 1000)
        yield Request(praise_url, callback=self.parse_praise, headers={"Referer": post_item["url"]},
                      meta={"post_item": post_item})

    def parse_praise(self, response):
        logger.info('praise  url is {}'.format(response.url))
        post_item = response.meta["post_item"]
        body = response.body[15:]
        info = json.loads(body)["UsefulList"]
        if len(info) == 0:
            post_item["praise_num"] = 0
        else:
            post_item["praise_num"] = info[0]["UsefulCount"]
        logger.info(post_item)
        dumper = CSVDumper("auto_qa_aodi.csv")
        dumper.process_item(CSVLineItem(columns=post_item), None)
        # yield post_item

    def get_text(self, response):
        # kw_map = self.pool.apply(parse_kw, (response.body.decode("gbk", "ignore"),))
        kw_map = parse_kw(response.body.decode("gbk", "ignore"))
        page = etree.HTML(response.body.decode("gbk", "ignore"))

        if page.xpath('//div[@id="maxwrap-maintopic"]//div[@class="w740"]'):
            content = page.xpath('//div[@id="maxwrap-maintopic"]//div[@class="w740"]')[0]
        else:
            return ''
        for script in content.xpath('.//script'):
            script.text = ''

        for style in content.xpath('.//style'):
            style.text = ''

        fs = page.xpath('//span[@style="font-family: myfont;"]')
        for font in fs:
            if font.text.strip() in kw_map:
                font.text = kw_map[font.text.strip()]
        return content.xpath('normalize-space()').replace('%nbsp', ' ')

    @property
    def random_ip(self):
        return "201.{}.{}.{}".format(random.randrange(256), random.randrange(256), random.randrange(256))


def parse_kw(content):
    try:
        url = TTF_PATTERN.findall(content)[0].strip()  # 提取 js 代码
        if url.startswith("//"):
            url = "http:" + url
        logger.debug("TTF file url: %s" % url)
        urllib.urlretrieve(url, ttf_file.name)
        time.sleep(random.random())
        font = TTFont(ttf_file.name)
        chars = list(set(etree.HTML(content).xpath('//span[@style="font-family: myfont;"]/text()')))
        logger.info("Chars: %s" % map(hex, map(ord, chars)))
        kw_content = {char: ttf_ocr(font, hex(ord(char)).upper().replace("0X", "uni")) for char in chars}
    except:
        logger.error(traceback.format_exc())
        return {}
    return kw_content


def ttf_ocr(font, key=None):
    gs = font.getGlyphSet()
    keys = [key for key in gs.keys() if key.startswith("uni")] if key is None else [key]
    c = []
    for i, key in enumerate(keys):
        if key not in gs:
            logger.info("No this key: %s" % key)
            c.append("")
            continue
        pen = ReportLabPen(gs, Path(fillColor=colors.black, strokeWidth=0.01))
        g = gs[key]
        g.draw(pen)
        w, h = 50, 50
        g = Group(pen.path)
        g.translate(10, 10)
        g.scale(0.02, 0.02)
        d = Drawing(w, h)
        d.add(g)
        renderPM.drawToFile(d, png_file.name, fmt="PNG")
        result = os.popen("tesseract %s stdout -l chi_sim -psm 5" % png_file.name).read().strip().decode("utf-8",
                                                                                                         "ignore")
        if len(result) != 1:
            result = os.popen("tesseract %s stdout -l chi_sim -psm 8" % png_file.name).read().strip().decode(
                "utf-8",
                "ignore")
        logger.info("key: %s, result: %s" % (key, result))
        c.append(result)
    if key is not None:
        return c[0]
    return c


class ReportLabPen(BasePen):
    """A pen for drawing onto a reportlab.graphics.shapes.Path object."""

    def __init__(self, glyphSet, path=None):
        BasePen.__init__(self, glyphSet)
        if path is None:
            path = Path()
        self.path = path

    def _moveTo(self, p):
        (x, y) = p
        self.path.moveTo(x, y)

    def _lineTo(self, p):
        (x, y) = p
        self.path.lineTo(x, y)

    def _curveToOne(self, p1, p2, p3):
        (x1, y1) = p1
        (x2, y2) = p2
        (x3, y3) = p3
        self.path.curveTo(x1, y1, x2, y2, x3, y3)

    def _closePath(self):
        self.path.closePath()
