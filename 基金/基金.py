#usr/bin/env python3
# -*- coding: utf-8 -*-
'guangfajijin'
__author__='maomaochong'

import requests
import json
import time
import numpy as np
from bs4 import BeautifulSoup

hd={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
    'Accept-Encoding':'gzip, deflate, sdch',
    'Accept-Language':'zh-CN,zh;q=0.8'
    }

class Funds_spyder(object):
    def __init__(self):
        print('----begin---')
    def net_value(self,url):
        page_source=requests.post(url)
        plain_text=page_source.text
        tst=json.loads(plain_text)
        print(tst)

if __name__=='__main__':
    s=Funds_spyder()
    s.net_value(url='http://www.gffunds.com.cn/apistore/JsonService?service=BaseInfo&method=Fund&op=queryFundByGFCategory')