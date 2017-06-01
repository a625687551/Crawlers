#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from bs4 import BeautifulSoup
import requests

__author__ = 'wangjiafneng'

start_url = 'http://www.555zw.com/book/4/4262/'
test_url = 'http://www.555zw.com/book/4/4262/787495.html'


def get_each_page(url):
    web_data = requests.get(url)
    web_data.encoding = "gbk"
    soup = BeautifulSoup(web_data.text, 'lxml')
    page = soup.select('tr > td > a')
    for singe in page:
        page_url = url + singe.get('href')
        page_name = singe.get_text('title')
        if u'更多' in page_name:
            continue
        print(page_url, page_name)
        return page_url


def get_page_info():
    web_data = requests.get(url)
    web_data.encoding = "gbk"
    soup = BeautifulSoup(web_data.text, 'lxml')
    title = soup.select('div.h1title h1')[0].text
    content = soup.select('div.contentbox')[0].text.split('show')[0]
    print(title, content)


get_each_page(start_url)
# get_page_info(test_url)
