# usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'wangjianfeng'

import requests
import re
import time
import http.cookiejar as cookielib
from selenium import webdriver
from bs4 import BeautifulSoup

# 构造一个头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36'}
ses = requests.session()


class ZH_Login():
    def __int__(self, username, password):
        self.username, self.password = str(username), str(password)
        # self.ses=requests.session()
        print(self.username, self.password)

    def get_xsrf(self):
        '''xsrf是一个动态参数，貌似不用提交也可以'''
        index_url = 'https://www.zhihu.com/'
        index_page = ses.get(index_url, headers=headers)
        html = index_page.text
        pattern = r'type="hidden" name="_xsrf" value="(.*?)"/>'
        _xsrf = re.findall(pattern=pattern, string=html)
        print(_xsrf[0])
        return _xsrf[0]

    def get_captcha(self):  # recoginize captcha
        pass

    def isLgoin(self):  # check login
        pass

    def login(self):  # login
        pass


if __name__ == '__main__':
    t = ZH_Login()
    t.get_xsrf()
