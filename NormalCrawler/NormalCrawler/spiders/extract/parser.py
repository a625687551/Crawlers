# -*- coding: utf-8 -*-

import re
import json
import time
import random
import socket
import logging
import tempfile
import traceback
import os
from threading import Timer
from multiprocessing import Process

import requests
from lxml import etree
from fontTools.ttLib import TTFont

logger = logging.getLogger(__name__)
DOWNLOAD_TTF_TIMEOUT = 10
TTF_PATTERN = re.compile(r"url\('([^']+?ttf)'\)")
ttf_file = tempfile.NamedTemporaryFile(suffix=".ttf")
socket.setdefaulttimeout(DOWNLOAD_TTF_TIMEOUT)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2986.0 Safari/537.36",
}


def gen_headers(referer=None):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2986.0 Safari/537.36",
    }
    if referer:
        headers["Referer"] = referer
    return headers
print(os.getcwd())
with open("font", "rb") as f:
    font_dict = json.loads(f.read())


def urlretrieve(url, filepath, refer):
    def download():
        response = requests.get(url, headers=gen_headers(refer), timeout=DOWNLOAD_TTF_TIMEOUT)
        with open(filepath, 'wb') as fh:
            fh.write(response.content)

    def kill(pc):
        logger.info("Stop download process.")
        pc.terminate()

    p = Process(target=download)
    p.start()
    t = Timer(DOWNLOAD_TTF_TIMEOUT, kill, (p,))
    t.start()
    p.join()
    t.cancel()


def parse_kw(content):
    try:
        url = TTF_PATTERN.findall(content)[0].strip()  # 提取 js 代码
        if url.startswith("//"):
            url = "http:" + url
        logger.info("TTF file url: %s" % url)
        time.sleep(random.random())
        urlretrieve(url, ttf_file.name, url)
        font = TTFont(ttf_file.name)
        bad_font = font.getReverseGlyphMap()
        chars = list(set(etree.HTML(content).xpath('//span[@style="font-family: myfont;"]/text()')))
        logger.info("Chars: %s" % map(hex, map(ord, chars)))
        # kw_content = {char: ttf_ocr(font, hex(ord(char)).upper().replace("0X", "uni")) for char in chars}
        kw_content = {char: font_dict.get(str(bad_font.get(char.upper().replace("&#X", "uni")))) for char in chars}
    except:
        logger.error(traceback.format_exc())
        return {}
    return kw_content


if __name__ == '__main__':
    logging.basicConfig(format="%(message)s", level=logging.DEBUG)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2986.0 Safari/537.36",
        "X-Forwarded-For": "123.21.23.1",
    }

    url = "http://club.autohome.com.cn/bbs/thread-c-4080-61996477-1.html"
    r = requests.get(url, headers=headers)
    kw = parse_kw(r.content.decode("gbk", "ignore"))
    doc = etree.HTML(r.content.decode("gbk", "ignore"))
    fs = doc.xpath('//span[@style="font-family: myfont;"]')
    print(fs)
    print(kw)
    # for font in fs:
    #     if font.text.strip() in kw:
    #         font.text = kw[font.text.strip()]
    # first_floor_content = doc.xpath('normalize-space(//div[@class="conttxt"])')
    # logger.info(first_floor_content)
