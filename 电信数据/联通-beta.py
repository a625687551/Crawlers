#!/usr/bin/env python
# encoding: utf-8


"""
@version: 0.2
@author: phpergao
@license: Apache Licence
@contact: endoffight@gmail.com
@site: http://www.phpgao.com
@software: PyCharm
@file: 10010.py
@time: 15-1-3 下午6:06
一键查询联通宽带余额
"""

import urllib
import http.cookiejar as cookielib
import json


class Crawl():
    def __init__(self, username, passwd, debug=False):
        (self.username, self.passwd) = (username, passwd)

        self.cookie = cookielib.CookieJar()
        cookieHandler = urllib.HTTPCookieProcessor(self.cookie)
        self.is_debug = debug
        if self.is_debug:

            httpHandler = urllib.HTTPHandler(debuglevel=1)
            httpsHandler = urllib.HTTPSHandler(debuglevel=1)
            opener = urllib.build_opener(cookieHandler, httpHandler, httpsHandler)

        else:
            opener = urllib.build_opener(cookieHandler)

        urllib.install_opener(opener)
        self.last_url = ''

    def get_html(self, url, postdata=''):

        print ("Requesting for %s" % url)

        if postdata != '':
            req = urllib.Request(url, postdata)
        else:
            req = urllib.Request(url)

        req.add_header('User-Agent', 'Mozilla/5.0 (Ubuntu; X11; Linux i686; rv:8.0) Gecko/20100101 Firefox/8.0')
        req.add_header('Content-Type', 'application/x-www-form-urlencoded')
        req.add_header('Cache-Control', 'no-cache')
        req.add_header('Accept', '*/*')
        req.add_header('Connection', 'Keep-Alive')

        try:
            resp = urllib.urlopen(req)
        except Exception as e:
            print (e)

        self.last_url = url
        if self.is_debug:
            print( "method: %s" % req.get_method())
            crawl.tell_cookie()

        return resp

    def tell_cookie(self):
        for item in self.cookie:
            print "cookie name : %s ---- value: %s" % (item.name, item.value)

    def get_balance(self):
        # 首页
        url_home = "http://www.10010.com/"
        # 登录主页
        url_login = "https://uac.10010.com/portal/mallLogin.jsp?redirectURL=http://www.10010.com"
        # 登录框架页
        url_frame = "https://uac.10010.com/portal/homeLogin"
        # 登录地址
        # 这里需要观察一下chrome的发送信息，需要自己改的有areaCode和arrcity
        # 就是登录时候选择的信息
        # 说是post，其实只是明文GET 囧
        # 无力吐槽
        url_post = "https://uac.10010.com/portal/Service/MallLogin?callback=jQuery172006519943638704717_" \
                   "1420279331097&redirectURL=http%3A%2F%2Fwww.10010.com&userName=" + str(self.username) + "&password=" \
                   + str(self.passwd) + "&pwdType=01&productType=04&redirectType=01&rememberMe=1&areaCode=841" \
                                        "&arrcity=%E8%A5%BF%E5%AE%89"
        'https://uac.10010.com/portal/Service/MallLogin?callback=jQuery172006519943638704717_" \
                   "1420279331097&redirectURL=http%3A%2F%2Fwww.10010.com&userName=" + str(self.username) + "&password=" \
                   + str(self.passwd) + "&pwdType=01&productType=04&redirectType=01&rememberMe=1&areaCode=841" \
                                        "&arrcity=%E8%A5%BF%E5%AE%89'

        # 点击查询按钮链接
        cookie1 = "http://iservice.10010.com/ehallService/static/login/r?menuid=000100010013"

        # 点击后获取到key为e3的cookie，参数可能会变
        # cookie2 = "http://iservice.10010.com/e3/static/check/checklogin/?_=1420301171070"
        cookie2 = 'http://iservice.10010.com/e3/static/check/checklogin/?_=1479956969513'


        # 查询余额页面
        url_balance = "http://iservice.10010.com/e3/query/account_balance.html"
        # 查询余额接口
        url_last = "http://iservice.10010.com/e3/static/query/accountBalance/search?"

        # self.get_html(url_home)
        # self.get_html(url_login)
        self.get_html(url_frame)
        self.get_html(url_post)
        self.get_html(url_home)
        self.get_html(cookie1)
        # a=1意思是将请求方法变为POST
        self.get_html(cookie2, "a=1")
        self.get_html(url_balance)

        return self.get_html(url_last, "a=1")


if __name__ == '__main__':
    crawl = Crawl(xxxxx, xxxxx)
    info = crawl.get_balance()

    data = json.load(info)
    print data['realtimebalance']
