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
from fontTools.ttLib import TTFont
from fontTools.pens.basePen import BasePen
from reportlab.lib import colors
from reportlab.graphics import renderPM
from reportlab.graphics.shapes import Path
from reportlab.graphics.shapes import Group, Drawing, scale
from pipelines.csv_dumper import CSVDumper, CSVLineItem

logger = logging.getLogger(__name__)
TTF_PATTERN = re.compile(r"url\('([^']+?ttf)'\)")
ttf_file = tempfile.NamedTemporaryFile(suffix=".ttf")
png_file = tempfile.NamedTemporaryFile(suffix=".png")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2986.0 Safari/537.36",
}
useful_url = "https://zhidao.autohome.com.cn/ajax/GetUsefulInfo?tid={tid}&rids={rids}&_={t}"


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
            result = os.popen("tesseract %s stdout -l chi_sim -psm 8" % png_file.name).read().strip().decode("utf-8",
                                                                                                             "ignore")
        logger.info("key: %s, result: %s" % (key, result))
        c.append(result)
    if key is not None:
        return c[0]
    return c


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


def fetch_content(url, referer=None):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2986.0 Safari/537.36",
        "X-Forwarded-For": "{}.{}.{}.{}".format(random.randrange(50, 100), random.randrange(256), random.randrange(256),
                                                random.randrange(256)),
    }
    if referer:
        headers["Referer"] = referer
    return requests.get(url, headers=headers).content.decode("gbk", "ignore")


def _load_lines(filepath):
    with open(filepath) as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines if line.strip()]
    return lines


def get_navs(url_list):
    for url in url_list:
        time.sleep(2)
        tid = re.findall(r"thread.*?-.*?-\d+-(\d+)", url)
        if tid:
            tid = tid[0]
        data_url = "https://zhidao.autohome.com.cn/ajax/ZhidaoForClubTopicMerge?tid={tid}".format(tid=tid)
        body = fetch_content(data_url, url)
        data_list = re.findall(r"var qaextend = ({.*?});", body)
        if data_list:
            data = json.loads(data_list[0])
            result = " > ".join(
                map(lambda x: data.get(x, "").strip(), ["brandName", "seriesName", "class1Name", "class2Name"]))
            print result
            return result
        else:
            # not a QA post
            return ""


def main():
    dumper = CSVDumper("auto_qa.csv")
    urls = _load_lines("u1s.txt")
    for url in urls:
        time.sleep(2)
        print "Request list url:", url
        content = fetch_content(url)
        doc = etree.HTML(content)
        hrefs = doc.xpath('//ul[@class="qa-list-con"]//a/@href')
        for href in hrefs:
            time.sleep(2)
            detail_url = urlparse.urljoin(url, href)
            print "Request detail url:", detail_url
            content = fetch_content(detail_url)
            kw = parse_kw(content)
            doc = etree.HTML(content)
            fs = doc.xpath('//span[@style="font-family: myfont;"]')
            for font in fs:
                if font.text.strip() in kw:
                    font.text = kw[font.text.strip()]
            title = doc.xpath('//div[@id="consnav"]/span[last()]/text()')[0]
            first_floor_content = doc.xpath('normalize-space(//div[@class="conttxt"])')
            second_floor_content = doc.xpath('normalize-space((//div[contains(@class, "x-reply")])[1])')
            tid = doc.xpath('//div[contains(@name, "replyuseful")]/@data-tid')[0]
            rid = doc.xpath('//div[contains(@name, "replyuseful")]/@data-rid')[0]
            classes = get_navs([detail_url])
            praise_url = useful_url.format(tid=tid, rids=rid, t=time.time()*1000)
            print "Request useful url :", praise_url
            praise_num = json.loads(fetch_content(praise_url, referer=detail_url)[15:])["UsefulList"][0]["UsefulCount"]

            print title
            print first_floor_content
            print second_floor_content
            print classes
            print praise_num
            dumper.process_item(CSVLineItem(columns={"title": title,
                                                     "Q": first_floor_content,
                                                     "A": second_floor_content,
                                                     "praise": praise_num,
                                                     "class": classes,
                                                     "url": detail_url}), None)


if __name__ == '__main__':
    main()
