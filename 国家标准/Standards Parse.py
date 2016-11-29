#usr/bin/env python3
# -*- coding:utf-8 -*-

__author__='wangjianfeng'

import requests
import pandas as pd
import re
import json
import time
from sqlalchemy import create_engine
from bs4 import BeautifulSoup
from selenium import webdriver

class phantomjs_SS(object):
    #
    def __int__(self,url):
        service_args = ['--proxy=localhost:1080', '--proxy-type=socks5', ]
        driver = webdriver.PhantomJS(executable_path="C:\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe",
                                     service_args=service_args)
        driver.get(url)
        self.soup = BeautifulSoup(driver.page_source, 'lxml')
        driver.close()
    #抓取spc.org.cn标准列表信息
    def spc_list(self):
        standard = []
        for x in self.soup.select(' div.search-left > div'):
            data = {}
            print(x.text())
            try:
                data['标准编号'] = list(x.stripped_strings)[0].split('\t')[-1]
                data['标准名称'] = list(x.stripped_strings)[1]
                pattern = r'(?:英文名称|发布日期|实施日期|读者对象|内容简介)\xa0:\n.*'
                for i in re.findall(pattern, x.get_text('\n', True)):
                    y = i.split('\xa0:\n')
                    data[y[0]] = y[1]
                standard.append(data)
            except:
                continue
        df = pd.DataFrame(standard, columns=['标准编号', '标准名称', '英文名称', '发布日期', '实施日期', '读者对象', '内容简介'])
        print(df)
        return df