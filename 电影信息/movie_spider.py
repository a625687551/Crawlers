# -*- coding: utf-8 -*-
"""
Created on Wed Jan 18 09:21:01 2017

@author: heting
"""
# %%
import json
import requests
from bs4 import BeautifulSoup
import base64
import re
import datetime
import time
import traceback
from urllib.parse import quote

# %%
session = requests.session()
url = 'http://www.jycinema.cn/frontUIWebapp/templates/default/cinema-detail.html?id=475'

resp = session.get(url)
soup = BeautifulSoup(resp.content, 'html.parser')

url = 'http://www.jycinema.cn/frontUIWebapp/appserver/cinCinemaMessageService/findCinema'
data = 'params=%7B%22cinemaId%22%3A%22475%22%2C%22type%22%3A%22queryAll%22%2C%22memberId%22%3A%22%22%2C%22channelCode%22%3A%22J0002%22%2C%22channelId%22%3A%223%22%7D'

headers = {'Accept': 'application/json, text/javascript, */*; q=0.01',
           'Accept-Encoding': 'gzip, deflate',
           'Accept-Language': 'zh-CN,zh;q=0.8',
           'Connection': 'keep-alive',
           'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
           'Host': 'www.jycinema.cn',
           'Origin': 'http//www.jycinema.cn',
           'Referer': 'http//www.jycinema.cn/frontUIWebapp/templates/default/cinema-detail.html?id=475',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
           'X-Requested-With': 'XMLHttpRequest'}

resp = session.post(url, headers=headers, data=bytes(data, 'utf-8'), timeout=None)

JSESSIONID_one = session.cookies.get_dict()['JSESSIONID']
soup = BeautifulSoup(resp.content, 'html.parser')

soup_info = json.loads(resp.text)

url = 'http://www.jycinema.cn/frontUIWebapp/appserver/PcCmsNoticeMessageService/findCmsNoticeMessage'

headers = {'Accept': 'application/json, text/javascript, */*; q=0.01',
           'Accept-Encoding': 'gzip, deflate',
           'Accept-Language': 'zh-CN,zh;q=0.8',
           'Connection': 'keep-alive',
           'Content-Length': '219',
           'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
           'Host': 'www.jycinema.cn',
           'Origin': 'http//www.jycinema.cn',
           'Referer': 'http//www.jycinema.cn/frontUIWebapp/templates/default/cinema-detail.html?id=475',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
           'X-Requested-With': 'XMLHttpRequest'}

data = 'params=%7B%22cinemaId%22%3A%22475%22%2C%22type%22%3A%22queryAll%22%2C%22memberId%22%3A%22%22%2C%22channelCode%22%3A%22J0002%22%2C%22channelId%22%3A%223%22%2C%22channelCode%22%3A%22J0002%22%2C%22channelId%22%3A%223%22%7D'
# session.cookies.pop('JSESSIONID')
resp = session.post(url, headers=headers, data=bytes(data, 'utf-8'), timeout=None)
JSESSIONID_two = session.cookies.get_dict()['JSESSIONID']
soup = BeautifulSoup(resp.content, 'html.parser')

url = 'http://www.jycinema.cn/frontUIWebapp/appserver/commonSaafImagesService/findImages'

headers = {'Accept': 'application/json, text/javascript, */*; q=0.01',
           'Accept-Encoding': 'gzip, deflate',
           'Accept-Language': 'zh-CN,zh;q=0.8',
           'Connection': 'keep-alive',
           'Content-Length': '175',
           'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
           'Host': 'www.jycinema.cn',
           'Origin': 'http//www.jycinema.cn',
           'Referer': 'http//www.jycinema.cn/frontUIWebapp/templates/default/cinema-detail.html?id=475',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
           'X-Requested-With': 'XMLHttpRequest'}

data = 'params=%7B%22targetId%22%3A%22475%22%2C%22targetType%22%3A%22CINEMA_PROPAGATE%22%2C%22imgChannel%22%3A%22PC%22%2C%22channelCode%22%3A%22J0002%22%2C%22channelId%22%3A%223%22%7D'
# session.cookies.pop('JSESSIONID')
resp = session.post(url, headers=headers, data=bytes(data, 'utf-8'), timeout=None)
soup = BeautifulSoup(resp.content, 'html.parser')
soup_info = json.loads(resp.text)
JSESSIONID_three = session.cookies.get_dict()['JSESSIONID']

url = 'http://api.map.baidu.com/?qt=dec&ie=utf-8&oue=1&fromproduct=jsapi&res=api&callback=BMap._rd._cbk2558&ak=tPjs1xtTnhqqzSg3Bpx286LWpFvjTC17'

headers = {'Accept': '*/*',
           'Accept-Encoding': 'gzip, deflate, sdch',
           'Accept-Language': 'zh-CN,zh;q=0.8',
           'Connection': 'keep-alive',
           'Host': 'api.map.baidu.com',
           'Referer': 'http//www.jycinema.cn/frontUIWebapp/templates/default/cinema-detail.html?id=475',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}

resp = session.get(url, headers=headers, timeout=None)
# soup = BeautifulSoup(resp.content.decode('gbk'),'html.parser')
pattern = re.compile(r'\{.*\}')
jsonObj = json.loads(re.findall(pattern, resp.text)[0])

url = 'http://www.jycinema.cn/frontUIWebapp/appserver/commonItemSkuService/getTime'
headers = {'Accept': 'application/json, text/javascript, */*; q=0.01',
           'Accept-Encoding': 'gzip, deflate',
           'Accept-Language': 'zh-CN,zh;q=0.8',
           'Connection': 'keep-alive',
           'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
           'Host': 'www.jycinema.cn',
           'Origin': 'http//www.jycinema.cn',
           'Referer': 'http//www.jycinema.cn/frontUIWebapp/templates/default/schedule.html?cinemaId=475',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
           'X-Requested-With': 'XMLHttpRequest'}

cityName = '全国'
data = 'params=' + quote(json.dumps({"type": "getTime", "cityName": cityName, "channelCode": "J0002", "channelId": "3"},
                                    ensure_ascii=False).replace(' ', ''))
session.cookies.set('JSESSIONID', JSESSIONID_one, path='/')
resp = session.post(url, headers=headers, data=bytes(data, 'utf-8'), timeout=None)
soup = BeautifulSoup(resp.content, 'html.parser')
session.cookies.get_dict()
resp.cookies.get_dict()

url = 'http://www.jycinema.cn/frontUIWebapp/appserver/commonItemSkuService/getTime'
headers = {'Accept': 'application/json, text/javascript, */*; q=0.01',
           'Accept-Encoding': 'gzip, deflate',
           'Accept-Language': 'zh-CN,zh;q=0.8',
           'Connection': 'keep-alive',
           'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
           'Host': 'www.jycinema.cn',
           'Origin': 'http//www.jycinema.cn',
           'Referer': 'http//www.jycinema.cn/frontUIWebapp/templates/default/schedule.html?cinemaId=475',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
           'X-Requested-With': 'XMLHttpRequest'}

# -------------------------->设置一个城市列表即可['成都'，'重庆'.....]
cityName = '成都'
data = 'params=' + quote(json.dumps({"type": "getTime", "cityName": cityName, "channelCode": "J0002", "channelId": "3"},
                                    ensure_ascii=False).replace(' ', ''))
resp = session.post(url, headers=headers, data=bytes(data, 'utf-8'), timeout=None)
soup = BeautifulSoup(resp.content, 'html.parser')
session.cookies.get_dict()
resp.cookies.get_dict()

url_cityid = 'http://www.jycinema.cn/frontUIWebapp/appserver/cinCinemaMessageService/findCinemaByCityName'

headers = {'Accept': 'application/json, text/javascript, */*; q=0.01',
           'Accept-Encoding': 'gzip, deflate',
           'Accept-Language': 'zh-CN,zh;q=0.8',
           'Connection': 'keep-alive',
           'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
           'Host': 'www.jycinema.cn',
           'Origin': 'http//www.jycinema.cn',
           'Referer': 'http//www.jycinema.cn/frontUIWebapp/templates/default/schedule.html?cinemaId=475',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
           'X-Requested-With': 'XMLHttpRequest'}

data = 'params=' + quote(
    json.dumps({"type": "totalCinema", "cityName": cityName, "channelCode": "J0002", "channelId": "3"},
               ensure_ascii=False).replace(' ', ''))
resp = session.post(url_cityid, headers=headers, data=bytes(data, 'utf-8'), timeout=None)

cityid = json.loads(resp.text)['data'][0]['cinemaData'][0]['cinemaId']

url_data = 'http://www.jycinema.cn/frontUIWebapp/appserver/commonItemSkuService/findItemSku'

cinemaId = str(cityid)  # ---->成都的id
data = 'params=' + quote(json.dumps(
    {"cinemaId": cinemaId, "showtime": "2017-01-18", "type": "queryItemSku", "memberLevelName": "", "memberId": "",
     "channelCode": "J0002", "channelId": "3"}, ensure_ascii=False).replace(' ', ''))

headers = {'Accept': 'application/json, text/javascript, */*; q=0.01',
           'Accept-Encoding': 'gzip, deflate',
           'Accept-Language': 'zh-CN,zh;q=0.8',
           'Connection': 'keep-alive',
           'Content-Length': '230',
           'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
           'Host': 'www.jycinema.cn',
           'Origin': 'http//www.jycinema.cn',
           'Referer': 'http//www.jycinema.cn/frontUIWebapp/templates/default/schedule.html?cinemaId=475',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
           'X-Requested-With': 'XMLHttpRequest'}

resp = session.post(url, headers=headers, data=bytes(data, 'utf-8'), timeout=None)
soup = BeautifulSoup(resp.content, 'html.parser')

GET_DATA = json.loads(resp.text)
