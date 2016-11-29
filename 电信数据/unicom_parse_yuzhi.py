#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import numpy as np
from numpy.random import randint

userName = str(18665961559)
password = '066530'
import time

# 查询详单请求url
url1 = 'http://iservice.10010.com/e3/static/query/callDetail?'

params1 = {
    'menuCode': '000100030001',
    'menuId': '000100030001'
}

# post参数---待完善
payload = {
    'pageNo': '1',
    'pageSize': '20',
    'beginDate': '2016-11-01',
    'endDate': '2016-11-24'
}
# 设置请求头---导入 'User-Agent' 列表让程序随机选择一个
headers = {

    'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:41.0) Gecko/20100101 Firefox/41.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0'
}

session = requests.Session()
session.headers = headers

# 查询详单请求url(正常情况请求)
url2 = 'http://iservice.10010.com/e3/static/query/callDetail?'
req_time = int(time.time() * 1000)

params4 = {
    '_': str(req_time),
    'accessURL': 'http://iservice.10010.com/e4/query/bill/call_dan-iframe.html?',
    'menuCode': '000100030001',
    'menuId': '000100030001',
    'menuid': '000100030001'
}

# GET请求的登录主页面请求URL
url_post = 'https://uac.10010.com/portal/Service/MallLogin?'

params2 = {
    'callback': 'jQuery17209332841114299033_' + str(req_time),
    'req_time': str(req_time),
    'redirectURL': 'http%3A%2F%2Fwww.10010.com',
    'userName': userName,
    'password': password,
    'pwdType': '01',
    'productType': '01',
    'redirectType': '01',
    'rememberMe': '1',
    '_': str(req_time + 1)
}

# 关键请求环节
url_semi = 'http://iservice.10010.com/e3/static/common/mall_info?'

params3 = {'callback': 'jsonp' + str(req_time)}

# 模拟请求登录----输入账号xxxx 密码xxxxx(必须要求是服务密码)
r1 = session.get(url_post, params=params2, headers=headers)
print('---登录成功---请等待1s')
time.sleep(1)

# 请求中间环节（获取授权）----输入账号xxxx 密码xxxxx(必须要求是服务密码)
r2 = session.get(url_semi, params=params3, headers=headers)
print('---访问中间页面成功---请等待1s')
time.sleep(1)

# 请求目标页面(详单查询)
r3 = session.get(url2, params=params4, cookies=r2.cookies)
time.sleep(1)
d = session.post(url1, params=params1, data=payload, headers=headers, cookies=r2.cookies)
print('---访问通话记录详情页面成功---请等待2s')

s = d.content.decode()
# 输出结果
print('数据结果：\n' + s)