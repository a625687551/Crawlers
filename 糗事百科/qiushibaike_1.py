#!usr/bin/env python3
# _*_ coding: utf-8 -*-

import requests
import json

from lxml import etree
from bs4 import BeautifulSoup


def get_info(url):
    s = requests.session()
    data = {
        "fastloginfield": "email",
        "username": "977729594@qq.com",
        "password": "yiquan0451",
        "quickforward": "yes",
        "handlekey": "ls"
    }

    html = s.post(url, data=data)
    test = s.get(url="http://www.bbsls.net/thread-2863490-1-1.html")
    print(test.cookies)
    # item_list = etree.XML(html.text)
    # content = etree.parse(html.text)
    # item_list = content.xpath('//div[@id="content-left"]/div')
    # for item in item_list.find_all()


if __name__ == '__main__':
    url = "http://www.bbsls.net/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes&inajax=1"
    get_info(url)
