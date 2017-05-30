#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'zhuxian_novel'

_author = 'wangjiafneng'

import time
from bs4 import BeautifulSoup
import requests, pymongo

client = pymongo.MongoClient('localhost', 27017)
zhuxian = client['zhuxian']
url_list = zhuxian['url_list']
page_content = zhuxian['page_content']

start_url = 'http://www.ybdu.com/xiaoshuo/2/2442/'
test_url = 'http://www.ybdu.com/xiaoshuo/2/2442/233740.html'


def get_eachpage(url):
    web_data = requests.get(url)
    web_data.encoding = "gbk"
    soup = BeautifulSoup(web_data.text, 'lxml')
    page = soup.select('ul.mulu_list li a')
    for singe in page:
        pageurl = url + singe.get('href')
        pagename = singe.get_text()
        print(pageurl, pagename)


def get_pageinfo(url):
    web_data = requests.get(url)
    web_data.encoding = "gbk"
    soup = BeautifulSoup(web_data.text, 'lxml')
    title = soup.select('div.h1title h1')[0].text
    content = soup.select('div.contentbox')[0].text.split('show')[0]
    print(title, content)


get_eachpage(start_url)
get_pageinfo(test_url)
